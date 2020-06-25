from bsa import Bsa

if __name__ == "__main__":
    bsa = Bsa()

    business_name = "wealthsimple"
    opts = {
        'refresh_cache': False,
        'print_results': True,
        'with_time_context': False
    }

    bsa.analyze(business_name, opts)
