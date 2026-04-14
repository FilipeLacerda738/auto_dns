#!/usr/bin/env python3

import subprocess
import sys
import os

PRESETS_DNS = [
    ("Cloudflare", ["1.1.1.1", "1.0.0.1"], ["2606:4700:4700::1111", "2606:4700:4700::1001"]),
    ("Google", ["8.8.8.8", "8.8.4.4"], ["2001:4860:4860::8888", "2001:4860:4860::8844"]),
    ("Quad9", ["9.9.9.9", "149.112.112.112"], ["2620:fe::fe", "2620:fe::9"]),
    ("OpenDNS", ["208.67.222.222", "208.67.220.220"], ["2620:119:35::35", "2620:119:53::53"]),
    ("AdGuard", ["94.140.14.14", "94.140.15.15"], ["2a10:50c0::ad1:ff", "2a10:50c0::ad2:ff"]),
    ("CleanBrowsing", ["185.228.168.168", "185.228.169.168"], ["2a0d:2a00:1::", "2a0d:2a00:2::"])
]


def verificar_root():
    if os.geteuid() != 0:
        print("Execute o programa com sudo.")
        sys.exit(1)


def obter_conexao_ativa():
    try:
        resultado = subprocess.run(
            ["nmcli", "-t", "-f", "NAME,DEVICE", "connection", "show", "--active"],
            capture_output=True,
            text=True
        )

        linhas = [l for l in resultado.stdout.strip().split("\n") if l]
        if not linhas:
            return None

        return linhas[0].split(":")[0]

    except Exception:
        return None


def obter_status_ipv6(conexao):
    try:
        resultado = subprocess.run(
            ["nmcli", "-g", "ipv6.method", "connection", "show", conexao],
            capture_output=True,
            text=True
        )
        return resultado.stdout.strip()
    except Exception:
        return "desconhecido"


def aplicar_dns(conexao, ipv4, ipv6):
    try:
        dns_ipv4 = " ".join(ipv4)
        dns_ipv6 = " ".join(ipv6)

        subprocess.run(["nmcli", "connection", "modify", conexao, "ipv4.ignore-auto-dns", "yes"], check=True)
        subprocess.run(["nmcli", "connection", "modify", conexao, "ipv4.dns", dns_ipv4], check=True)
        
        status_ipv6 = obter_status_ipv6(conexao)

        if status_ipv6 == "disabled":
            print("IPv6 está desativado → aplicando apenas DNS IPv4")
        else:
            try:
                subprocess.run(["nmcli", "connection", "modify", conexao, "ipv6.ignore-auto-dns", "yes"], check=True)
                subprocess.run(["nmcli", "connection", "modify", conexao, "ipv6.dns", dns_ipv6], check=True)
                print("IPv6 ativo → DNS IPv6 aplicado")
            except subprocess.CalledProcessError:
                print("Falha ao aplicar IPv6 → continuando apenas com IPv4")

        subprocess.run(["nmcli", "connection", "up", conexao], check=True)

        print("\nDNS aplicado com sucesso!")

    except subprocess.CalledProcessError as erro:
        print(f"Erro ao aplicar DNS: {erro}")


def mostrar_menu():
    print("\n==============================")
    print("      DNS SWITCHER    ")
    print("==============================\n")

    for indice, (nome, _, _) in enumerate(PRESETS_DNS, start=1):
        print(f"{indice}. {nome}")

    print("0. Sair")


def main():
    verificar_root()

    conexao = obter_conexao_ativa()
    if not conexao:
        print("Não foi possível detectar a conexão ativa.")
        sys.exit(1)

    print(f"Conexão ativa: {conexao}")

    while True:
        mostrar_menu()

        try:
            escolha = int(input("\nEscolha um DNS: "))
        except ValueError:
            print("Entrada inválida.")
            continue

        if escolha == 0:
            print("Saindo...")
            break

        if 1 <= escolha <= len(PRESETS_DNS):
            nome, ipv4, ipv6 = PRESETS_DNS[escolha - 1]

            print(f"\nAplicando DNS: {nome}")

            aplicar_dns(conexao, ipv4, ipv6)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
