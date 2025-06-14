from typing import Final

from playwright.sync_api import expect

from ..generic_constants import actions, properties
from ..onboarding import School
from ..playwright_ops import PlaywrightOperations

from .dashboard import DashboardPage


class ChildrenPage:
    CHILD1: Final[str] = "CFILTER1, CFilter1"
    LBL_CHILD_RECORD: Final[str] = "1 child"

    LBL_CHILDREN: Final[str] = "Children"
    LBL_HEADING: Final[str] = "heading"
    LBL_MAIN: Final[str] = "main"
    LBL_TABLE_HEADERS: Final[str] = (
        "Name and NHS number	Postcode	School	Date of birth"
    )
    TXT_SEARCH: Final[str] = "Search"
    BTN_SEARCH: Final[str] = "Search"
    LNK_CLEAR_FILTERS: Final[str] = "Clear filters"
    LNK_CHILD_RECORD: Final[str] = "Child record"
    LNK_CHILD_MAV_853: Final[str] = "MAV_853, MAV_853"
    LNK_CHILD_CHANGE_NHSNO: Final[str] = "CHANGENHSNO, CHANGENHSNO"
    LNK_EDIT_CHILD_RECORD: Final[str] = "Edit child record"
    LNK_CHANGE_NHS_NO: Final[str] = "Change   NHS number"
    BTN_CONTINUE: Final[str] = "Continue"
    BTN_REMOVE_FROM_COHORT: Final[str] = "Remove from cohort"

    def __init__(
        self, playwright_operations: PlaywrightOperations, dashboard_page: DashboardPage
    ):
        self.po = playwright_operations
        self.dashboard_page = dashboard_page

    def verify_headers(self):
        self.po.verify(
            locator=self.LBL_HEADING,
            property=properties.TEXT,
            expected_value=self.LBL_CHILDREN,
            exact=True,
        )
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value=self.LBL_TABLE_HEADERS,
        )

    def verify_filter(self):
        self.po.act(locator=self.TXT_SEARCH, action=actions.FILL, value=self.CHILD1)
        self.po.act(locator=self.BTN_SEARCH, action=actions.CLICK_BUTTON)
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value=self.LBL_CHILD_RECORD,
        )

    def verify_child_has_been_uploaded(self, child_list) -> None:
        if len(child_list) >= 1:
            self.dashboard_page.click_mavis()
            self.dashboard_page.click_children()
            for _child_name in child_list:
                self.search_for_a_child(child_name=_child_name)

    def search_for_a_child(self, child_name: str) -> None:
        self.po.act(locator=self.TXT_SEARCH, action=actions.FILL, value=child_name)
        self.po.act(locator=self.BTN_SEARCH, action=actions.CLICK_BUTTON)
        self.po.verify(
            locator=self.LBL_MAIN, property=properties.TEXT, expected_value=child_name
        )

    def click_tab(self, name: str):
        link = self.po.page.get_by_role("navigation").get_by_role("link", name=name)
        link.click()
        link.get_by_role("strong").wait_for()

    def click_activity_log(self):
        self.click_tab("Activity log")

    def verify_activity_log_for_created_or_matched_child(
        self, child_name: str, location: str, *, is_created: bool
    ):
        self.po.act(locator=self.TXT_SEARCH, action=actions.FILL, value=child_name)
        self.po.act(locator=self.BTN_SEARCH, action=actions.CLICK_BUTTON)
        self.po.act(locator=child_name, action=actions.CLICK_LINK)

        self.click_activity_log()

        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value="Consent given",
        )
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value=f"Invited to the session at {location}",
        )

        # FIXME: Update this text when MAVIS-1896/MAV-253 is closed
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value="Consent response manually matched with child record",
        )

    def verify_mav_853(self, school: School):
        """
        1. Upload vaccination records for a patient that doesn't contain vaccine information (VACCINE_GIVEN column)
        2. Navigate to the patient, either in a session or from the global children view
        3. Expected: patient details can be seen
        Actual: crash
        """
        self.search_for_a_child(child_name=self.LNK_CHILD_MAV_853)
        self.po.act(locator=self.LNK_CHILD_MAV_853, action=actions.CLICK_LINK)

        self.click_activity_log()

        expect(
            self.po.page.get_by_role("heading", name="Vaccinated with Gardasil 9").first
        ).to_be_visible()

        # Verify vaccination record
        self.po.act(locator=self.LNK_CHILD_RECORD, action=actions.CLICK_LINK)

        self.po.page.get_by_role("row").filter(has_text=str(school)).get_by_role(
            "link", name="Gardasil 9 (HPV)"
        ).click()

        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value="Outcome	Vaccinated",
        )

    def change_nhs_no(self):
        self.search_for_a_child(child_name=self.LNK_CHILD_CHANGE_NHSNO)
        self.po.act(locator=self.LNK_CHILD_CHANGE_NHSNO, action=actions.CLICK_LINK)
        self.po.act(locator=self.LNK_EDIT_CHILD_RECORD, action=actions.CLICK_LINK)
        self.po.act(locator=self.LNK_CHANGE_NHS_NO, action=actions.CLICK_LINK)
        # self.po.act(
        #     locator="locator('div').filter(has_text=re.compile(r'What is the child’s NHS number\?$')).click()",
        #     action=framework_actions.CHAIN_LOCATOR_ACTION,
        # )
        self.po.act(
            locator=self.LNK_CHILD_CHANGE_NHSNO, action=actions.FILL, value="9123456789"
        )
        self.po.act(locator=self.BTN_CONTINUE, action=actions.CLICK_BUTTON)
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value="Enter a valid NHS number",
        )

    def remove_child_from_cohort(self, child_name: str):
        _expected_message = f"{child_name} removed from cohort"
        self.search_for_a_child(child_name=child_name)
        self.po.act(locator=child_name, action=actions.CLICK_LINK)
        self.po.act(locator=self.BTN_REMOVE_FROM_COHORT, action=actions.CLICK_BUTTON)
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value=_expected_message,
        )
