# profiles/validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class SymbolValidator:
    def validate(self, password, user=None):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Password must contain at least one symbol."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Your password must contain at least one special symbol.")
