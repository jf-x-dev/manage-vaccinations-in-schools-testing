from typing import Final

from ..generic_constants import actions, properties
from ..mavis_constants import Vaccine
from ..playwright_ops import PlaywrightOperations
from ..wrappers import get_current_datetime, get_offset_date


class VaccinesPage:
    LBL_VACCINE_NAME: Final[str] = "Gardasil 9 (HPV)"
    LBL_VACCINE_MANUFACTURER: Final[str] = "Merck Sharp & Dohme"
    LBL_MAIN: Final[str] = "main"
    LBL_PARAGRAPH: Final[str] = "paragraph"
    LBL_BATCH_ARCHIVED: Final[str] = "Batch archived."
    TXT_BATCH_NAME: Final[str] = "Batch"
    TXT_EXPIRY_DAY: Final[str] = "Day"
    TXT_EXPIRY_MONTH: Final[str] = "Month"
    TXT_EXPIRY_YEAR: Final[str] = "Year"
    BTN_ADD_BATCH: Final[str] = "Add batch"
    BTN_SAVE_CHANGES: Final[str] = "Save changes"
    BTN_CONFIRM_ARCHIVE: Final[str] = "Yes, archive this batch"

    def __init__(self, playwright_operations: PlaywrightOperations):
        self.po = playwright_operations

    def verify_current_vaccine(self):
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value=self.LBL_VACCINE_NAME,
            exact=False,
        )
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value=self.LBL_VACCINE_MANUFACTURER,
            exact=False,
        )

    def _calculate_batch_details(self, vaccine: Vaccine):
        self.batch_name = f"{vaccine.replace(' ', '')}{get_current_datetime()}"
        self.future_expiry_date = get_offset_date(offset_days=365)
        self.day = self.future_expiry_date[-2:]
        self.month = self.future_expiry_date[4:6]
        self.year = self.future_expiry_date[:4]

    def add_batch(self, vaccine: Vaccine):
        self._calculate_batch_details(vaccine)
        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value=vaccine,
        )

        self.po.page.get_by_role("link", name=f"Add a new {vaccine} batch").click()

        self.po.verify(
            locator=self.LBL_MAIN,
            property=properties.TEXT,
            expected_value=vaccine,
        )
        self.po.act(
            locator=self.TXT_BATCH_NAME, action=actions.FILL, value=self.batch_name
        )
        self.po.act(locator=self.TXT_EXPIRY_DAY, action=actions.FILL, value=self.day)
        self.po.act(
            locator=self.TXT_EXPIRY_MONTH, action=actions.FILL, value=self.month
        )
        self.po.act(locator=self.TXT_EXPIRY_YEAR, action=actions.FILL, value=self.year)
        self.po.act(locator=self.BTN_ADD_BATCH, action=actions.CLICK_BUTTON)
        _success_message = f"Batch {self.batch_name} added"
        self.po.verify(
            locator=self.LBL_PARAGRAPH,
            property=properties.TEXT,
            expected_value=_success_message,
        )

    def change_batch(self, vaccine: Vaccine):
        batch_name = str(vaccine) if self.batch_name == "" else self.batch_name
        self.po.act(
            locator=batch_name, action=actions.CLICK_LINK_INDEX_FOR_ROW, index=0
        )  # CHANGE link
        self.po.act(
            locator=self.TXT_EXPIRY_YEAR,
            action=actions.FILL,
            value=get_offset_date(offset_days=730)[:4],
        )
        self.po.act(locator=self.BTN_SAVE_CHANGES, action=actions.CLICK_BUTTON)
        _success_message = f"Batch {self.batch_name} updated"
        self.po.verify(
            locator=self.LBL_PARAGRAPH,
            property=properties.TEXT,
            expected_value=_success_message,
        )

    def archive_batch(self, vaccine: Vaccine):
        batch_name = str(vaccine) if self.batch_name == "" else self.batch_name

        self.po.act(
            locator=batch_name, action=actions.CLICK_LINK_INDEX_FOR_ROW, index=1
        )  # ARCHIVE link
        self.po.act(locator=self.BTN_CONFIRM_ARCHIVE, action=actions.CLICK_BUTTON)
        self.po.verify(
            locator=self.LBL_PARAGRAPH,
            property=properties.TEXT,
            expected_value=self.LBL_BATCH_ARCHIVED,
        )
