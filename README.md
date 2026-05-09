<div align="center">

<h1>DNS Switcher</h1>

<p>
Aplicativo em Python para alterar rapidamente servidores DNS no Linux usando NetworkManager.
</p>

<img src="https://img.shields.io/badge/python-3.x-blue">
<img src="https://img.shields.io/badge/platform-linux-green">
<img src="https://img.shields.io/badge/license-MIT-yellow">

</div>

<hr>

<h2>Funcionalidades</h2>

<ul>
  <li>Suporte a IPv4</li>
  <li>Suporte a IPv6</li>
  <li>Fallback automático</li>
  <li>Detecção automática de conexão ativa</li>
  <li>Integração com nmcli</li>
  <li>Compatível com Ethernet e Wi-Fi</li>
</ul>

<hr>

<h2>DNS disponíveis</h2>

<table>
  <tr>
    <th>Provedor</th>
    <th>IPv4</th>
    <th>IPv6</th>
  </tr>

  <tr>
    <td>Cloudflare</td>
    <td>1.1.1.1 / 1.0.0.1</td>
    <td>Sim</td>
  </tr>

  <tr>
    <td>Google</td>
    <td>8.8.8.8 / 8.8.4.4</td>
    <td>Sim</td>
  </tr>

  <tr>
    <td>Quad9</td>
    <td>9.9.9.9 / 149.112.112.112</td>
    <td>Sim</td>
  </tr>

  <tr>
    <td>OpenDNS</td>
    <td>208.67.222.222 / 208.67.220.220</td>
    <td>Sim</td>
  </tr>

  <tr>
    <td>AdGuard</td>
    <td>94.140.14.14 / 94.140.15.15</td>
    <td>Sim</td>
  </tr>

  <tr>
    <td>CleanBrowsing</td>
    <td>185.228.168.168 / 185.228.169.168</td>
    <td>Sim</td>
  </tr>

</table>

<hr>

<h2>Requisitos</h2>

<ul>
  <li>Linux</li>
  <li>Python 3</li>
  <li>NetworkManager</li>
  <li>nmcli</li>
</ul>

<hr>

<h2>Instalação</h2>

<p>Clone o repositório:</p>

<pre>
git clone https://github.com/FilipeLacerda738/auto_dns.git
</pre>

<p>Entre na pasta:</p>

<pre>
cd dns-switcher
</pre>

<p>Dê permissão de execução:</p>

<pre>
chmod +x dns-switcher.py
</pre>

<hr>

<h2>Instalação global</h2>

<pre>
sudo cp dns-switcher.py /usr/local/bin/dns-switcher
sudo chmod +x /usr/local/bin/dns-switcher
</pre>

<p>Agora execute:</p>

<pre>
dns-switcher
</pre>

<hr>

<h2>Como usar</h2>

<pre>
sudo dns-switcher
</pre>

<p>Exemplo:</p>

<pre>
==============================
        DNS SWITCHER
==============================

1. Cloudflare
2. Google
3. Quad9
4. OpenDNS
5. AdGuard
6. CleanBrowsing
0. Sair
</pre>

<hr>

<h2>IPv6</h2>

<p>
Se o IPv6 estiver desativado ou configurado como <code>ignore</code>,
o script perguntará se deseja ativá-lo automaticamente.
</p>

<br>
<hr>

<h2>Verificando DNS atual</h2>

<pre>
nmcli dev show | grep DNS
</pre>

<p>ou:</p>

<pre>
resolvectl status
</pre>

<hr>

<h2>Restaurar DNS automático</h2>

<pre>
nmcli connection modify "&lt;Suaconexao&gt;" ipv4.ignore-auto-dns no
nmcli connection modify "&lt;Suaconexao&gt;" ipv6.ignore-auto-dns no
nmcli connection up "&lt;Suaconexao&gt;"
</pre>


<hr>

<h2>Melhorias futuras</h2>

<ul>
  <li>DNS-over-HTTPS</li>
  <li>DNS-over-TLS</li>
  <li>Benchmark automático de latência</li>
  <li>Interface TUI</li>
  <li>Sistema de logs</li>
  <li>Backup automático de DNS</li>
</ul>

<hr>

<h2>Segurança</h2>

<p>
O script altera apenas configurações locais de rede utilizando nmcli.
Nenhuma informação é enviada para serviços externos.
</p>

<hr>

<h2>Licença</h2>

<p>MIT License</p>

<hr>

<div align="center">

<h3>Desenvolvido por Filipe</h3>

</div>
