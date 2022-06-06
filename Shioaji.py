import shioaji as sj

api = sj.Shioaji()
api.login(
    person_id="YOUR_ID",
    passwd="YOUR_PASSWORD",
    contracts_cb=lambda security_type: print(f"{repr(security_type)} fetch done.")
)