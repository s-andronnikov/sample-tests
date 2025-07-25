Python package versions:
 - python: >=3.12
 - pytest: >=8.4
 - playwright: >=v1.53
Python package manager is poetry >= 2.0.
Base JS UI frameworks is:
 - react: >=18.3
 - ag-grid-enterprise: >=34
 - ag-grid-react: >=34

Testing framework is pytest + playwright-python (sync version)

Base Tests structures:
 - Types of tests:
   - API: folder /api
   - UI: folder /ui

Currently need to work with UI tests only.
UI tests stricture:
 - All tests located at /ui/tests folder and can be separated by following modules:
   - folder "tax_depreciation": urls with __host__/depreciation/*
   - folder "dit": urls with {host_url}/dit/*
   - folder "provision": urls with {host_url}/provision/*
   - folder "nova": urls with {host_url}/nova/*
 - Each test files should has tests associated to page. Pages located at ui/pages and should be separated by modules in tests way (see folders naming above).
 - Each isolated element on page like list grid or form can be isolated as separated component. Components located as /ui/pages/components
   and should be located using module/page folders structure (see module folders naming above).

Helpers located: /ui/helpers
 - url_helper.py: helper to build url using defined routes from UIRoutes (common/routes.py) and dynamic variables like "depr_case_id"
 - ag_grid_helper.py: common helper with locators and actions for Ag-Grid grids.

Fixtures initialisation located at: ui/fixtures.py. Do not use
second one authenticated fixture with login action injections.

config.py - define configuration variables

All tests should use AI instructions, project context for UI tests and existed tests as an example.
