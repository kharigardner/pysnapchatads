from __future__ import absolute_import, annotations, print_function, unicode_literals, with_statement
import requests
import typing
import collections

from pysnapchatads.helpers import build_url
import pysnapchatads.objects.user as user
import pysnapchatads.errors as errors
import pysnapchatads.objects.organizations as orgs
import pysnapchatads.objects.ad_accounts as ad_accountz

class SnapchatMarketing(object):
    """Base class for Snapchat Marketing API Access"""

    def __init__(
            self, 
            access_token: str, 
            proxies: typing.Optional[collections.MutableMapping[str, str]] = None
        ) -> None:
        
        self.access_token: str = access_token
        self.BASE_URL: str = 'https://adsapi.snapchat.com/v1'
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})

        if proxies:
            self.session.proxies.update(proxies)


    def get_authenticated_user(self) -> user.User:
        """
        This endpoint retrieves information about the Snapchat user that
        is represented by the access token used, the information includes
        the snapchat_username.
        
        More information: https://marketingapi.snapchat.com/docs/#user
        """

        return user.User.from_json(
            api_client=self,
            json_data=self.session.get(
                url='https://adsapi.snapchat.com/v1/me'
            ).json()['me']
        )
    
    ########################
    # API Patterns
    ########################

    def _get_many_entities(
            self,
            plural_parent_entity_name: str,
            parent_entity_id: str,
            plural_entity_name: str,
            **kwargs
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        Pattern to retrieve multiple entities from the API.

        More information: https://marketingapi.snapchat.com/docs/#get-many-entities
        """

        url: str = build_url(
            base_url=self.BASE_URL,
            endpoint=plural_parent_entity_name,
            path=f'{parent_entity_id}/{plural_entity_name}',
        )

        if 'limit' in kwargs:
            params: typing.Dict[str, int] = {'limit': typing.cast(int, kwargs['limit'])}
            first_response = self.session.get(
                url=url,
                params=params
            )

        else:
            first_response: requests.Response = self.session.get( # type: ignore
                url=url
            )

        first_response.raise_for_status()

        if 'limit' not in kwargs:
            return first_response.json()[plural_entity_name]
        
        results: typing.List[typing.Dict[str, typing.Any]] = self._paginator(
            response_json=first_response.json(),
            response_data_key=plural_entity_name
        )
        return results
        
    def _get_single_entity(
            self,
            plural_entity_name: str,
            entity_id: str,
            **kwargs 
    ) -> typing.Dict[str, typing.Any]:
        """
        Pattern to retrieve a single entity from the API.
        
        More information: https://marketingapi.snapchat.com/docs/#get-a-single-entity
        """
        url: str = build_url(
                    base_url=self.BASE_URL,
                    endpoint=plural_entity_name,
                    path=entity_id
                )
        
        result = self.session.get(
            url=url
        )

        return result.json()[plural_entity_name]
        
            

    
    def _paginator(
            self,
            response_json: typing.Dict[str, typing.Any],
            response_data_key: str
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        Pattern to paginate through an API endpoint.
        
        More information: https://marketingapi.snapchat.com/docs/#pagination
        """
        
        result_bag: typing.List = []

        while True:
            try:
                result_bag.extend(response_json[response_data_key])
            except KeyError:
                break
            if "next_link" not in response_json["paging"]:
                break
            try:
                response = self.session.get(
                    url=response_json["paging"]["next_link"]
                )
                response.raise_for_status()
                response_json = response.json()
            except Exception as e:
                raise errors.PaginationError() from e
            
        return typing.cast(typing.List[typing.Dict[str, typing.Any]], result_bag)
    

    def _create_entities(
            self,
            plural_parent_entity_name: str,
            parent_entity_id: str,
            plural_entity_name: str,
            data: typing.List[typing.Dict[str, typing.Any]],
            **kwargs
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The Create endpoints support bulk creation, 
        meaning you can create several objects at the same time as long as they share the same parent. 
        For example, you can create muliple Campaigns within a single Ad Account in a single POST request.

        More information: https://marketingapi.snapchat.com/docs/#create-one-or-more-entities
        """

        url: str = build_url(
            base_url=self.BASE_URL,
            endpoint=plural_parent_entity_name,
            path=f'{parent_entity_id}/{plural_entity_name}'
        )

        results = self.session.post(
            url=url,
            json=data
        )
        
        results.raise_for_status()

        
        return results.json()[plural_entity_name]
    

    def _update_entities(
            self,
            plural_parent_entity_name: str,
            parent_entity_id: str,
            plural_entity_name: str,
            data: typing.List[typing.Dict[str, typing.Any]],
            **kwargs
    ) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        The Update endpoints support bulk update, 
        meaning you can update several objects at the same time as long as they share the same parent. 
        For example, you can update muliple Campaigns within a single Ad Account in a single PUT request.

        More Information: https://marketingapi.snapchat.com/docs/#update-one-or-more-entities
        """

        url: str = build_url(
            base_url=self.BASE_URL,
            endpoint=plural_parent_entity_name,
            path=f'{parent_entity_id}/{plural_entity_name}'
        )

        results = self.session.put(
            url=url,
            json=data
        )

        results.raise_for_status()

        return results.json()[plural_entity_name]
    
    def _delete_entity(
            self,
            plural_entity_name: str,
            entity_id: str
    ) -> None:
        """
        Delete a single entity.
        
        More information: https://marketingapi.snapchat.com/docs/#delete-a-single-entity
        """

        url: str = build_url(
            base_url=self.BASE_URL,
            endpoint=plural_entity_name,
            path=entity_id
        )

        self.session.delete(
            url=url
        )
    
    ########################
    # Organizations
    ########################

    def list_organizations(
            self,
            with_ad_accounts: bool = False
    ) -> typing.Union[typing.List[typing.Tuple[orgs.Organization, typing.List[ad_accountz.AdAccount]]], typing.List[orgs.Organization]]:
        """
        List all organizations the currently authenticated user has access to.
        Optionally, can return a tuple of organizations and associated ad accounts.

        More information: https://marketingapi.snapchat.com/docs/#list-organizations
        """

        response_data: requests.Response = self.session.get(
            url=f'{self.BASE_URL}/me/organizations',
            params={'with_ad_accounts': with_ad_accounts} if with_ad_accounts else None
        )

        response_data.raise_for_status()

        if not with_ad_accounts:
            return [
                orgs.Organization.from_json(
                    api_client=self,
                    json_data=org
                )
                for org in response_data.json()['organizations']
            ]
        
        with typing.cast(typing.Dict[str, typing.Union[str, typing.Any, typing.Dict[str, typing.Any]]], response_data.json()) as data:

                ad_accounts = data['organizations']['ad_accounts']
                org = data['organizations']

                # remove the ad_accounts key from the org
                typing.cast(typing.Dict[str, typing.Any],org).pop('ad_accounts')

                return [
                    (
                        orgs.Organization.from_json(
                            api_client=self,
                            json_data=org
                        ),
                        [
                            ad_accountz.AdAccount.from_json(
                                api_client=self,
                                json_data=ad_account
                            )
                            for ad_account in ad_accounts
                        ]
                    )
                for org in data['organizations']
                ]
        

    def get_organization(
            self,
            organization_id: str
    ) -> orgs.Organization:
        """
        Get a single organization.

        More information: https://marketingapi.snapchat.com/docs/#get-a-specific-organization
        """

        return orgs.Organization.from_json(
            api_client=self,
            json_data=self._get_single_entity(
                plural_entity_name='organizations',
                entity_id=organization_id
            )
        )
    
    ########################
    # Ad Accounts
    ########################

    def get_single_ad_account(
            self,
            ad_account_id: str
    ) -> ad_accountz.AdAccount:
        """
        Get a single ad account.
        """

        return ad_accountz.AdAccount.from_json(
            api_client=self,
            json_data=self._get_single_entity(
                plural_entity_name='adaccounts',
                entity_id=ad_account_id
            )
        )