from models.host import HostModel


def print_report(hosts: list[HostModel]):

    print(f"[+] Audit Completed For {len(hosts)} host(s)")
    for host in hosts:
        print(
            f"\n[*] We Found {len(host.users)} user(s) in host {host.hostname}\n")

        print(
            f"{'Username':<20}"
            f"{'UID':<10}"
            "Password Expires"
        )

        print("-" * 50)

        for user in host.users:
            print(
                f"{user.username:<20}"
                f"{user.uid:<10}"
                f"{user.expires}"
            )
