from datetime import datetime, timedelta
import logging
import requests

from homeassistant.const import (
    CONF_NAME,
)
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import (
    generate_entity_id,
    Entity,
)

_LOGGER = logging.getLogger(__name__)

CONF_PROCUCT = "product"

PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PROCUCT): cv.string,
    }
)
ENTITY_ID_FORMAT = "sensor.{}"
COINBASE_PRO_PROVIDER = CoinbaseProDataProvider()

def setup_platform(hass, config, add_entities, disc_info=None):
    """Set up the Coinbase Pro platform."""
    entity_id = generate_entity_id(ENTITY_ID_FORMAT, "crypto_" + conf[CONF_PROCUCT], hass=hass)
    entities = []
    entities.append(CoinbaseCryptoInfoSensor(entity_id, conf[CONF_PROCUCT], COINBASE_PRO_PROVIDER))
    add_entities(entities, False)


class CoinbaseCryptoInfoSensor(Entity):
    """A device for getting the next waste date."""

    def __init__(self, entity_id, product, provider):
        """Create the CoinbaseCryptoInfoSensor Sensor."""
        self.product = product
        self._price = None
        self._provider = provider
        self.entity_id = entity_id

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        return None

    @property
    def icon(self):
        """Return the icon to use in the frontend"""
        return "mdi:bitcoin"

    @property
    def state(self):
        """Return the state"""
        return self._price

    @property
    def device_class(self):
        """Return the device class"""
        return None

    @property
    def name(self):
        """Return the name of the entity."""
        return self.product

    @property
    def should_poll(self):
        """Determine if the component should be polled or not"""
        return False

    async def async_set_price(self, price):
        """Set new price."""
        self._price = price
        await self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Subscribe to Websocket events."""
        await super().async_added_to_hass()
        await self._provider.subscribe(self)


class CoinbaseProDataProvider(object):
    async def subscribe(entity):
        """Subscribe to Websocket events"""

        response = requests.get("https://api.pro.coinbase.com/products/BTC-EUR/ticker")
        body = response.json()
        entity.async_set_price(body["price"])
