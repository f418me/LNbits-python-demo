import asyncio
import logging
import ssl
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

        # Invoice to pay
        ln_invoice = 'lnbc110n1pnz54zwsp5xq4l3qdqy964zy839q56qck7v593df4n9fkzau245dvgxgq8l9gqpp5llekhypwuaemetgjrpjvca0j65eyyucpv5rafghdusqdjy0ykpsqdq523jhxapq2pshjmt9de6qxqyjw5qcqpjrzjqtc63jrkql6ptj8j9sq9jvqzwav5rh4y3p5uugcfdte8kr8aes9kjz6m2vqqsacqqyqqqqqqqqqqqeqqjq9qxpqysgqud5asfwh8re72dk2q6gr6esw2ch32atvpsk9g9ehsp8u84855l68cu4wh27a2ycmk04gwcagt0t0nmajr8qfvr8dvn9rj9qgenq5pzsp5wzk39'
        if ln_invoice is not None and ln_invoice.startswith('lnbc'):
            log.info("Lightning Invoice found:")
            log.info(ln_invoice)
        else:
            log.info('String contains no Lightning Invoice')
            ln_invoice = ''

        log.info(f'Clean LN Invoice:' + ln_invoice)
        decoded = await uw.get_decoded(ln_invoice)
        log.debug(decoded)

        if 'message' in decoded:
            if decoded['message'] == 'Failed to decode':
                logging.warning(F'Invoice decoding failed with message: ' + decoded['message'])
                is_valid = False
        else:
            is_valid = True

        if is_valid:
            amount = 0
            if 'amount_msat' in decoded:
                amount = int(int(decoded['amount_msat']) / 1000)
            if amount == 0:
                log.info('Amount 0 or not set: ' + str(amount))
            elif amount <= int(config.MAX_AMOUNT):
                res = await uw.pay_invoice(True, ln_invoice)

                if 'payment_hash' in res:
                    log.info('Payment done. Response is: ' + str(res))
                else:
                    log.info('Payment could not be don. Response is: ' + str(res))
            else:
                log.info('Amount to high: ' + str(amount))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
