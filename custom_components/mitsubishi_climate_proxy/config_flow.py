## config_flow.py — Config Flow for Mitsubishi Climate Proxy
## Role: UI-based configuration wizard for adding proxy instances via HA integrations page.
## Deps: homeassistant.config_entries, homeassistant.components.climate, homeassistant.components.select

import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_SOURCE
# Importiamo il modulo selector nativo di HA
from homeassistant.helpers import selector

from . import DOMAIN

CONF_HORIZONTAL_VANE_ENTITY = "horizontal_vane_entity"
_LOGGER = logging.getLogger(__name__)

class MitsubishiHybridConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Mitsubishi Hybrid Climate."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(f"{user_input[CONF_SOURCE]}_hybrid")
            self._abort_if_unique_id_configured()

            # Se l'utente non ha selezionato nulla per il wide vane, ripuliamo il dato
            if not user_input.get(CONF_HORIZONTAL_VANE_ENTITY):
                user_input[CONF_HORIZONTAL_VANE_ENTITY] = None

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, user_input[CONF_SOURCE]),
                data=user_input
            )

        # Definiamo lo schema usando i selettori nativi di Home Assistant
        data_schema = vol.Schema({
            # Selettore nativo per mostrare SOLO entità di tipo Climate
            vol.Required(CONF_SOURCE): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="climate")
            ),

            # Campo testo semplice per il nome personalizzato
            vol.Optional(CONF_NAME): selector.TextSelector(),

            # Selettore nativo per mostrare SOLO entità di tipo Select (il WideVane)
            # multiple=False e l'impostazione nativa permettono di lasciarlo vuoto
            vol.Optional(CONF_HORIZONTAL_VANE_ENTITY): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="select")
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )