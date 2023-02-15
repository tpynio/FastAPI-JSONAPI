from http import HTTPStatus
from typing import (
    List,
    Union,
)

from fastapi import Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from examples.api_for_sqlalchemy.extensions.sqlalchemy import Connector
from examples.api_for_sqlalchemy.helpers.factories.meta_base import FactoryUseMode
from examples.api_for_sqlalchemy.helpers.factories.user_bio import UserBioFactory, ErrorCreateUserBioObject
from examples.api_for_sqlalchemy.helpers.updaters.exceptions import ObjectNotFound

# from examples.api_for_sqlalchemy.helpers.updaters.update_user import UpdateUserBio, ErrorUpdateUserBioObject
from examples.api_for_sqlalchemy.models.schemas import UserBioSchema, UserBioPatchSchema
from examples.api_for_sqlalchemy.models.schemas.user_bio import UserBioInSchema
from examples.api_for_sqlalchemy.models import UserBio
from fastapi_rest_jsonapi import SqlalchemyEngine
from fastapi_rest_jsonapi.exceptions import (
    BadRequest,
    HTTPException,
)
from fastapi_rest_jsonapi.querystring import QueryStringManager
from fastapi_rest_jsonapi.schema import JSONAPIResultListSchema, JSONAPIResultDetailSchema
from fastapi_rest_jsonapi.views.detail_view import DetailViewBase
from fastapi_rest_jsonapi.views.list_view import ListViewBase


class UserBioDetail(DetailViewBase):
    async def get(
        self,
        obj_id,
        query_params: QueryStringManager,
        session: AsyncSession = Depends(Connector.get_session),
    ) -> JSONAPIResultDetailSchema:
        dl = SqlalchemyEngine(
            schema=self.jsonapi.schema_detail,
            model=self.jsonapi.model,
            session=session,
        )
        view_kwargs = {"id": obj_id}
        return await self.get_detailed_result(
            dl=dl,
            view_kwargs=view_kwargs,
            query_params=query_params,
        )

    # @classmethod
    # async def patch(
    #     cls,
    #     obj_id,
    #     data: UserBioPatchSchema,
    #     query_params: QueryStringManager,
    #     session: AsyncSession = Depends(Connector.get_session),
    # ) -> UserBioSchema:
    #     user_bio_obj: UserBio
    #     try:
    #         user_bio_obj = await UpdateUserBio.update(
    #             obj_id,
    #             data.dict(exclude_unset=True),
    #             query_params.headers,
    #             session=session,
    #         )
    #     except ErrorUpdateUserBioObject as ex:
    #         raise BadRequest(ex.description, ex.field)
    #     except ObjectNotFound as ex:
    #         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.description)
    #
    #     user = UserBioSchema.from_orm(user_bio_obj)
    #     return user


class UserBioList(ListViewBase):
    async def get(
        self,
        query_params: QueryStringManager,
        session: AsyncSession = Depends(Connector.get_session),
    ) -> JSONAPIResultListSchema:
        dl = SqlalchemyEngine(
            schema=self.jsonapi.schema_list,
            model=self.jsonapi.model,
            session=session,
        )
        return await self.get_paginated_result(
            dl=dl,
            query_params=query_params,
        )

    async def post(
        self,
        data: UserBioInSchema,
        query_params: QueryStringManager,
        session: AsyncSession = Depends(Connector.get_session),
    ) -> JSONAPIResultDetailSchema:
        try:
            user_bio_obj = await UserBioFactory.create(
                data=data.dict(),
                mode=FactoryUseMode.production,
                header=query_params.headers,
                session=session,
            )
        except ErrorCreateUserBioObject as ex:
            raise BadRequest(ex.description, ex.field)

        dl = SqlalchemyEngine(
            schema=self.jsonapi.schema_detail,
            model=self.jsonapi.model,
            session=session,
        )
        view_kwargs = {"id": user_bio_obj.id}
        return await self.get_detailed_result(
            dl=dl,
            view_kwargs=view_kwargs,
            query_params=query_params,
        )
