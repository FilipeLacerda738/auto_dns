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

METODOS_IPV6_VALIDOS = ["auto", "manual"]


def verificar_root():
    if os.geteuid() != 0:
        print("Execute o programa com sudo.")
        sys.exit(1)


def executar_comando(comando):
    return subprocess.run(
        comando,
        capture_output=True,
        text=True
    )


def obter_conexao_ativa():
    try:
        resultado = executar_comando(
            ["nmcli", "-t", "-f", "NAME,DEVICE,TYPE", "connection", "show", "--active"]
        )

        linhas = [l for l in resultado.stdout.strip().split("\n") if l]

        if not linhas:
            return None

        prioridade = ["ethernet", "wifi"]

        for tipo in prioridade:
            for linha in linhas:
                partes = linha.split(":")

                if len(partes) >= 3 and partes[2] == tipo:
                    return partes[0]

        return linhas[0].split(":")[0]

    except Exception:
        return None


def obter_status_ipv6(conexao):
    try:
        resultado = executar_comando(
            ["nmcli", "-g", "ipv6.method", "connection", "show", conexao]
        )

        return resultado.stdout.strip()

    except Exception:
        return "desconhecido"


def perguntar_ativacao_ipv6(conexao):
    while True:
        resposta = input(
            "\nIPv6 está desativado/ignorado.\n"
            "Deseja ativar IPv6 automaticamente? (s/n): "
        ).strip().lower()

        if resposta in ["s", "sim"]:
            try:
                subprocess.run(
                    ["nmcli", "connection", "modify", conexao, "ipv6.method", "auto"],
                    check=True
                )

                print("IPv6 ativado com sucesso.")

                return True

            except subprocess.CalledProcessError as erro:
                print(f"Erro ao ativar IPv6: {erro}")
                return False

        elif resposta in ["n", "nao", "não"]:
            print("Continuando apenas com IPv4...")
            return False

        else:
            print("Resposta inválida. Digite 's' ou 'n'.")


def aplicar_dns_ipv4(conexao, ipv4):
    dns_ipv4 = " ".join(ipv4)

    subprocess.run(
        ["nmcli", "connection", "modify", conexao, "ipv4.ignore-auto-dns", "yes"],
        check=True
    )

    subprocess.run(
        ["nmcli", "connection", "modify", conexao, "ipv4.dns", dns_ipv4],
        check=True
    )

    print("DNS IPv4 aplicado com sucesso.")


def aplicar_dns_ipv6(conexao, ipv6):
    status_ipv6 = obter_status_ipv6(conexao)

    if status_ipv6 not in METODOS_IPV6_VALIDOS:
        print(f"\nIPv6 indisponível ({status_ipv6})")

        ativado = perguntar_ativacao_ipv6(conexao)

        if not ativado:
            return

        status_ipv6 = obter_status_ipv6(conexao)

        if status_ipv6 not in METODOS_IPV6_VALIDOS:
            print("IPv6 ainda não está disponível.")
            return

    dns_ipv6 = " ".join(ipv6)

    try:
        subprocess.run(
            ["nmcli", "connection", "modify", conexao, "ipv6.ignore-auto-dns", "yes"],
            check=True
        )

        subprocess.run(
            ["nmcli", "connection", "modify", conexao, "ipv6.dns", dns_ipv6],
            check=True
        )

        print("DNS IPv6 aplicado com sucesso.")

    except subprocess.CalledProcessError as erro:
        print(f"Falha ao aplicar IPv6: {erro}")
        print("Continuando apenas com IPv4...")


def reativar_conexao(conexao):
    try:
        subprocess.run(
            ["nmcli", "connection", "up", conexao],
            check=True
        )

        print("Conexão reativada com sucesso.")

    except subprocess.CalledProcessError as erro:
        print(f"Erro ao reativar conexão: {erro}")
        sys.exit(1)


def aplicar_dns(conexao, ipv4, ipv6):
    try:
        aplicar_dns_ipv4(conexao, ipv4)

        aplicar_dns_ipv6(conexao, ipv6)

        reativar_conexao(conexao)

        print("\nDNS aplicado com sucesso!")

    except subprocess.CalledProcessError as erro:
        print(f"\nErro ao aplicar DNS: {erro}")


def mostrar_menu():
    print("\n==============================")
    print("        DNS SWITCHER")
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