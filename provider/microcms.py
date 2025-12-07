from typing import Any
import requests

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class MicrocmsProvider(ToolProvider):

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        service_domain = credentials.get("service_domain", "").strip()
        api_key = credentials.get("api_key", "").strip()

        if not service_domain:
            raise ToolProviderCredentialValidationError("Service domain is required")
        if not api_key:
            raise ToolProviderCredentialValidationError("API key is required")

        try:
            # Test API connection with a simple request
            url = f"https://{service_domain}.microcms.io/api/v1"
            headers = {"X-MICROCMS-API-KEY": api_key}

            # Try to get API info (this will fail if credentials are invalid)
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 401:
                raise ToolProviderCredentialValidationError("Invalid API key")
            elif response.status_code == 404:
                raise ToolProviderCredentialValidationError("Invalid service domain")
            elif response.status_code >= 400:
                raise ToolProviderCredentialValidationError(f"API error: {response.status_code}")

        except requests.RequestException as e:
            if "401" in str(e):
                raise ToolProviderCredentialValidationError("Invalid API key")
            elif "404" in str(e):
                raise ToolProviderCredentialValidationError("Invalid service domain")
            else:
                raise ToolProviderCredentialValidationError(f"Connection error: {str(e)}")
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

    #########################################################################################
    # If OAuth is supported, uncomment the following functions.
    # Warning: please make sure that the sdk version is 0.4.2 or higher.
    #########################################################################################
    # def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    #     """
    #     Generate the authorization URL for microcms OAuth.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR AUTHORIZATION URL GENERATION HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return ""
        
    # def _oauth_get_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    # ) -> Mapping[str, Any]:
    #     """
    #     Exchange code for access_token.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR CREDENTIALS EXCHANGE HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return dict()

    # def _oauth_refresh_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    # ) -> OAuthCredentials:
    #     """
    #     Refresh the credentials
    #     """
    #     return OAuthCredentials(credentials=credentials, expires_at=-1)
