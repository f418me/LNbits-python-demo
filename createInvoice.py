import asyncio
import logging
from aiohttp.client import ClientSession
from pylnbits.user_wallet import UserWallet
from pylnbits.config import Config as LNBitsConfig
from config import Config

config = Config()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=str(config.LOG_LEVEL))
log = logging.getLogger(__name__)
log.setLevel(config.LOG_LEVEL_INT)

async def main():
    # INITIALIZE the pylnbits with your config file
    c = LNBitsConfig(in_key=config.LNBITS_IN_KEY, admin_key=config.LNBITS_ADMIN_KEY, lnbits_url=config.LNBITS_URL)
    url = c.lnbits_url
    log.debug(f"url: {url}")
    log.debug(f"headers: {c.headers()}")
    log.debug(f"admin_headers: {c.admin_headers()}")


    async with ClientSession() as session:
        # GET wallet details
        uw = UserWallet(c, session)
        user_wallet = await uw.get_wallet_details()
        log.info(f"user wallet info : {user_wallet}")

        # CREATE an invoice
        # amount in Sats
        invoice_amount = 12
        invoice_message = "Test Invoice"
        invoice_webhook = "https://f418.me"
        res = await uw.create_invoice(False, invoice_amount, invoice_message, invoice_webhook)
        log.info('Invoice created. Response is: ' + str(res))
        ln_invoice = res['payment_request']
        log.info('Invoice is: ' + str(ln_invoice))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
