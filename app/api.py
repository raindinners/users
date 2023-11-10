from __future__ import annotations

from typing import Any, Dict, Optional

import jwt
from corecrud import Options, Returning, Values, Where
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from authorization import get_user_id_failed
from core.crud import crud
from core.depends import get_session
from core.settings import auth_settings, bot_settings
from orm import BalanceModel, UserModel
from requests import AuthRequest, TelegramAuthRequest, UpdateBalanceRequest
from responses import SignUpResponse, UserResponse
from schema import ApplicationResponse
from utils import verify_telegram_authorization

router = APIRouter()


async def sign_in_core(session: AsyncSession, request: TelegramAuthRequest) -> UserModel:
    user = await crud.users.select.one(
        Where(UserModel.telegram_id == request.id),
        session=session,
    )
    if not user:
        user = await crud.users.insert.one(
            Values(request.model_dump(exclude={"hash", "auth_date"}, by_alias=True)),
            Returning(UserModel),
            session=session,
        )
        await crud.balances.insert.one(
            Values({BalanceModel.user_id: user.id}),
            Returning(BalanceModel.id),
            session=session,
        )

    return user


@router.post(
    path="/signIn",
    response_model=ApplicationResponse[SignUpResponse],
    status_code=status.HTTP_200_OK,
)
async def sign_in(
    session: AsyncSession = Depends(get_session),
    request: TelegramAuthRequest = Body(...),
) -> Dict[str, Any]:
    verify_telegram_authorization(request=request, bot_token=bot_settings.BOT_TOKEN)

    user = await sign_in_core(session=session, request=request)

    return {
        "ok": True,
        "result": {
            "access_token": jwt.encode(
                payload={
                    "sub": user.id,
                },
                key=auth_settings.SECRET_KEY,
                algorithm=auth_settings.ALGORITHM,
            ),
        },
    }


async def get_user_core(session: AsyncSession, user_id: int) -> Optional[UserModel]:
    return await crud.users.select.one(
        Where(UserModel.id == user_id), Options(selectinload(UserModel.balance)), session=session
    )


async def get_user(
    authorization: AuthRequest = Body(...),
    session: AsyncSession = Depends(get_session),
) -> UserModel:
    user = await get_user_core(
        user_id=authorization.user_id
        if authorization.user_id
        else get_user_id_failed(access_token=authorization.access_token),
        session=session,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="USER_NOT_EXISTS",
        )

    return user


@router.post(
    path="/getMe",
    response_model=ApplicationResponse[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_authorization_information(user: UserModel = Depends(get_user)) -> Dict[str, Any]:
    return {
        "ok": True,
        "result": user,
    }


@router.post(
    path="/getUser",
    response_model=ApplicationResponse[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_information(user: UserModel = Depends(get_user)) -> Dict[str, Any]:
    return {
        "ok": True,
        "result": user,
    }


@router.post(
    path="/getBonus",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def get_bonus(
    session: AsyncSession = Depends(get_session),
    request: AuthRequest = Body(...),
) -> Dict[str, Any]:
    user = await get_user_core(
        session=session, user_id=get_user_id_failed(access_token=request.access_token)
    )
    if not user.balance.is_bonus():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="BONUS_NOT_AVAILABLE",
        )

    await crud.balances.update.one(
        Values({BalanceModel.balance: user.balance + BalanceModel.BONUS}),
        Where(BalanceModel.id == user.balance.id),
        Returning(BalanceModel.id),
        session=session,
    )

    return {
        "ok": True,
        "result": True,
    }


@router.post(
    path="/updateBalance",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def update_balance(
    session: AsyncSession = Depends(get_session),
    request: UpdateBalanceRequest = Body(...),
) -> Dict[str, Any]:
    user = await get_user_core(
        session=session, user_id=get_user_id_failed(access_token=request.access_token)
    )
    await crud.balances.update.one(
        Values({BalanceModel.balance: user.balance.balance + request.balance}),
        Where(BalanceModel.id == user.balance.id),
        Returning(BalanceModel.id),
        session=session,
    )

    return {
        "ok": True,
        "result": True,
    }
