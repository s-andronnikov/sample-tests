from config import base_settings
from common.routes import UIRoutes


class UrlHelper:
    """Helper class for generating URLs for UI routes"""

    @staticmethod
    def build_url(route: str, *args, **kwargs) -> str:
        """Build a URL for a UI route

        Args:
            route: The route template from UIRoutes
            *args: Positional arguments to format into the route
            **kwargs: Keyword arguments to format into the route

        Returns:
            Fully formatted URL
        """
        formatted_route = route

        # Handle positional args if provided
        if args:
            formatted_route = route.format(*args)
        # Handle keyword args if provided
        elif kwargs:
            formatted_route = route.format(**kwargs)

        return formatted_route.lstrip("/")

    @staticmethod
    def build_full_url(route: str, *args, **kwargs) -> str:
        """Build a full URL including protocol and host

        Args:
            route: The route template from UIRoutes
            *args: Positional arguments to format into the route
            **kwargs: Keyword arguments to format into the route

        Returns:
            Full URL including protocol and host
        """
        path = UrlHelper.build_url(route, *args, **kwargs)
        return f"{base_settings.protocol}://{base_settings.host}/{path}"

    @classmethod
    def depreciation_asset_class(cls, depr_case_id: str) -> str:
        """Build URL for depreciation asset class page

        Args:
            depr_case_id: The depreciation ID

        Returns:
            URL path for the depreciation asset class page
        """
        return cls.build_full_url(UIRoutes.DEPRECIATION_ASSET_CLASS, depr_case_id)

    @classmethod
    def depreciation_basis_adjustment(cls, depr_case_id: str) -> str:
        """Build URL for depreciation basis adjustment page

        Args:
            depr_case_id: The depreciation ID

        Returns:
            URL path for the depreciation basis adjustment page
        """
        return cls.build_full_url(UIRoutes.DEPRECIATION_BASIS_ADJUSTMENT, depr_case_id)

    @classmethod
    def depreciation_bonus_profile(cls, depr_case_id: str) -> str:
        """Build URL for depreciation bonus profile page

        Args:
            depr_case_id: The depreciation ID

        Returns:
            URL path for the depreciation bonus profile page
        """
        return cls.build_full_url(UIRoutes.DEPRECIATION_BONUS_PROFILE, depr_case_id)

    @classmethod
    def user_details(cls, user_id: str) -> str:
        """Build URL for user details page

        Args:
            user_id: The user ID

        Returns:
            URL path for the user details page
        """
        return cls.build_url(UIRoutes.USER_DETAILS, user_id)

    @classmethod
    def contact_details(cls, contact_id: str) -> str:
        """Build URL for contact details page

        Args:
            contact_id: The contact ID

        Returns:
            URL path for the contact details page
        """
        return cls.build_url(UIRoutes.CONTACT_DETAILS, contact_id)
