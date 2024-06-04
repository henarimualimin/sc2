import requests
from colorama import init, Fore, Style
import time

# Inisialisasi colorama untuk penggunaan warna
init(autoreset=True)

def read_wallet_addresses_from_file(filename):
    with open(filename, 'r') as file:
        addresses = [line.strip() for line in file if line.strip()]
    return addresses

def check_balance(wallet_addresses, token_contract_address, network):
    balances = {}
    api_keys = {
        "BSC": "QG3BDMFF3VXQTGYUDPS2N99XYYTP1P2ZIS",
        "ETH": "SRPWNBJPC1UMYHM5E5QNRFY8V3GJHCUVSK",
        "Polygon": "2WQUK21TYRJKTGEZJEG4IIHZ38U1R1FJUM"
    }
    if network not in api_keys:
        return "Error: Invalid network"

    api_key = api_keys[network]

    if network == "BSC":
        api_url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={token_contract_address}&address={{}}&tag=latest&apikey={api_key}"
    elif network == "ETH":
        api_url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={token_contract_address}&address={{}}&tag=latest&apikey={api_key}"
    elif network == "Polygon":
        api_url = f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={token_contract_address}&address={{}}&tag=latest&apikey={api_key}"

    try:
        for idx, address in enumerate(wallet_addresses, start=1):
            print(f"\n{Fore.YELLOW}[+] Checking balance  {idx}: {address}")

            # Warna yang berbeda untuk setiap wallet
            if idx % 3 == 0:
                print(Fore.GREEN, end="")
            elif idx % 3 == 1:
                print(Fore.BLUE, end="")
            else:
                print(Fore.RED, end="")

            response = requests.get(api_url.format(address))
            data = response.json()

            # Menambahkan warna pada pesan result dan status
            if data["status"] == "1":
                print(Fore.GREEN + f"{Fore.GREEN}[✓] Result:", data["result"])
                print(Fore.YELLOW + f"{Fore.YELLOW}[+] Status:", data["status"])
            else:
                print(Fore.RED + f"{Fore.RED}[X] Error:", data["message"])

            if data["status"] == "1":
                balance = int(data["result"]) / 10**18  # Convert balance from wei to token's decimals
                if balance == 0:
                    balances[address] = "Token balance: 0 (Zero balance)"
                else:
                    token_name = "Token"
                    if network == "BSC":
                        token_name = "BNB"
                    elif network == "ETH":
                        token_name = "ETH"
                    elif network == "Polygon":
                        token_name = "MATIC"
                    balances[address] = f"Saldo {token_name}: {balance} di {network}"
            else:
                balances[address] = "Error: " + data["message"]

            # Tambahkan garis panjang sebagai jeda antara alamat dengan warna biru
            print(Fore.BLUE + "-" * 50)

            # Waktu istirahat antara pengecekan setiap wallet
            time.sleep(1)

        return balances
    
    except Exception as e:
        return "Error: " + str(e)

print(f"{Fore.YELLOW}[+] Masukkan nama file txt address: ")
filename = input()
print(f"{Fore.YELLOW}[+] Masukkan Contract: ")
token_contract_address = input()
print(f"{Fore.YELLOW}[+] Masukkan jaringan (BSC, ETH, atau Polygon): ")
network = input()

wallet_addresses = read_wallet_addresses_from_file(filename)
balances = check_balance(wallet_addresses, token_contract_address, network)

for address, balance in balances.items():
    print(Fore.RESET, end="")
    print(f"{balance}, Wallet address: {address}")