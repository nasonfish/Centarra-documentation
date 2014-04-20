from jinja2 import Template

structs = {}

class JsonTable():
    a = {}
    def __init__(self):
        self.a = {}
        pass
    def add(self, name, desc, example):
        self.a[name] = {"desc": desc, "example": example}
        return self
    def add_lst(self, name, table):
        self.a[name] = {"table": table}
        return self
    def example(self, example):
        self.example = example
        return self

    def magic(self):
        frmt = Template("""
        <style>
        .tb:nth-child(even){ background-color: #ccc; }
        .tb:nth-child(odd){ background-color: #fff; }
        </style>
        <table>
        <tr>
        <th style="width: 15%;">Key</th>
        <th style="width: 55%;">Description</th>
        <th style="width: 30%;">Example</th>
        </tr>
        {% for i in a %}
            {% if "example" in a[i] %}
            <tr class="tb">
                <td>{{ i }}</td>
                <td>{{ a[i].desc }}</td>
                <td>{{ a[i].example }}</td>
            </tr>
            {% else %}
            <tr class="tb">
                <td>{{ i }}</td>
                <td colspan=2>{{ a[i].table.magic() }}</td>
            </tr>
            {% endif %}
        {% endfor %}
        </table>
        """)
        return frmt.render(a=self.a)

structs['invoice'] = JsonTable().add("payment_ts", "Unix timestamp representing the time the invoice was paid; null if the invoice is unpaid.", "Integer: 1375213382; None"
).add("user", "Username of the user who the invoice applies to - probably you.", "String: nasonfish"
).add("invoice", "Unique ID of the invoice you are viewing.", "Integer: 928",
).add("creation_ts", "Unix timestamp representing the time the invoice was created.", "Integer: 1375200553"
).add("total", "Number representing the total value of the invoice (0 if the invoice is paid).", "Float: 6.75"
).add_lst("items", JsonTable(
    ).add("line_item", "Unique ID of this line item.", "Integer: 1344"
    ).add("entry_ts", "Unix timestamp of the time this line item was created.", "Integer: 1375471700"
    ).add("description", "Description of this specific line item.", "String: Renewal, Paypal Payment, Service credit, Bitcoin payment, or other description."
    ).add("btc_price", "A representation of the price that was exchanged in this invoice, in Bitcoins (BTC)", "Float: -0.013937066402378594"
    ).add("price", "A representation of the price that was exchanged in this invoice, in USD.", "Float: -6.75"
    ).add("invoice", "Unique ID of the invoice that holds this line item.", "Integer: 928")
).example("""
{
    "items": [
        {
            "line_item": 1344,
            "entry_ts": 1375213382,
            "description": "Service credit (per nenolod)",
            "btc_price": -0.013937066402378594,
            "price": -6.75,
            "invoice": 928
        },
        {
            "line_item": 1430,
            "entry_ts": 1375471700,
            "description": "PayPal Payment - 36797038V8008391C",
            "btc_price": -0.013937066402378594,
            "price": -6.75,
            "invoice": 928
        }
    ],
    "payment_ts": 1375213382,
    "user": "nasonfish",
    "invoice": 928,
    "creation_ts": 1375200553,
    "total": -6.75
}""")

structs['vps'] = JsonTable().add_lst("profile",
          JsonTable().add("name", "A name representing your boot profile", "String: PV-GRUB (64-bit)"
          ).add("id", "A unique ID assigned to your current boot profile.", "Integer: 1")
).add("ipv6_limit", "The maximum amount of IPv6 addresses that can be assigned to your vServer.", "Integer: 1, 32"
).add("node", "The name of the current node your vServer exists on.", "String: dal2"
).add("name", "The internal name for your server, usually named as <your username>-<incrementing id>.", "String, nasonfish-1"
).add("ipv4_limit", "The maximum amount of IPv4 addresses that can be assigned to your vServer.", "Integer: 1"
).add("memory", "The amount of RAM that has been allocated to your vServer, in megabytes.", "Integer: 256"
).add("cpu_sla", "Your server's priority on claiming resources - this can be bulk if you are a high memory user.", "String: standard, bulk"
).add_lst("ips[]",
          JsonTable().add("ip", "The full IP address assigned to your server.", "String: 198.52.199.3"
          ).add("id", "The unique ID assigned to this specific IP address.", "Integer: 4006"
          ).add_lst("ipnet",
                    JsonTable().add("broadcast", "The broadcast address for this IP address", "String: 198.52.199.255"
                    ).add("netmask", "The netmask for this IP address", "String: 255.255.255.0"
                    ).add("version", "The Internet Protocol Version this IP address resembles", "Integer: 4, 6"
                    ).add("gateway", "The gateway address for this IP address", "String: 198.52.199.1",
                    ).add("network", "The IP address network this address resembles", "String: 198.52.199.0/24")
          )
).add("mac", "The MAC hardware address for your vServer", "String: 00:16:3e:8c:fa:f2"
).add("wss_metrics_uri", "The WSS metrics URI assigned to this vServer", "URI: wss://console-dal2.tortois.es:9393/stats/nasonfish-1/<hexidecimal_key>"
).add("user", "The username of the user this vServer is assigned to. Probably you.", "String: nasonfish"
).add("wss_console_uri", "The WSS console URI assigned to this vServer", "URI: wss://console-dal2.tortois.es:9393/console/nasonfish-1/<hexidecimal_key>"
).add("monitoring", "If Watchdog monitoring is enabled (meaning your server will be restarted automatically)", "Boolean: true, false",
).add("disk", "The amount of space allocated to your vServer, in gigabytes.", "Integer: 15"
).add("nickname", "The custom nickname assigned to your vServer.", "String: personal_vps"
).add("id", "A unique identifier for this vServer.", "Integer: 2830"
).add("swap", "The amount of SWAP this server has allocated.", "Integer: 256"
).example("""
{
    "vpslist": [
        {
            "profile": {
                "name": "PV-GRUB (64-bit)",
                "id": 1
            },
            "ipv6_limit": 1,
            "node": "dal2",
            "name": "nasonfish-1",
            "ipv4_limit": 1,
            "memory": 256,
            "cpu_sla": "standard",
            "ips": [
                {
                    "ip": "198.52.200.62",
                    "id": 4006,
                    "ipnet": {
                        "broadcast": "198.52.200.255",
                        "netmask": "255.255.255.0",
                        "version": 4,
                        "gateway": "198.52.200.1",
                        "network": "198.52.200.0/24"
                    }
                }
            ],
            "mac": "00:16:3e:8c:fa:f2",
            "wss_metrics_uri": "wss://console-dal2.tortois.es:9393/stats/nasonfish-1/<hex_string>",
            "user": "nasonfish",
            "wss_console_uri": "wss://console-dal2.tortois.es:9393/console/nasonfish-1/<hex_string>",
            "monitoring": false,
            "disk": 15,
            "nickname": "nasonfish",
            "id": 2830,
            "swap": 256
        }
    ]
}""")