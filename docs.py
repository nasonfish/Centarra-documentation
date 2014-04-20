from structures import structs
from jinja2 import Template

BASE_URL = "https://billing.centarra.com"

points = []

class Endpoint():
    def __init__(self, point, description, inp=None, **kwargs):
        self.point = point
        self.description = description
        self.inp = inp
        self.reply = kwargs
        points.append(self)
        self.out()

    def parse_end(self):
        tmp = Template("""{% if reply %}
        <table>
          <tr>
            <th>Key</th>
            <th>Value</th>
          </tr>
          {% for i in reply %}
          <tr>
            <td>{{ i }}{{ "[]" if reply[i].ls else "" }}</td>
            <td>{{ structs[reply[i].desc].magic() if not reply[i].raw else reply[i].desc }}</td>
          </tr>
          {% endfor %}
        </table>
        {% endif %}""")
        return tmp.render(reply=self.reply, structs=structs)

    def parse_inp(self):
        tmp = Template("""
        {% if inp %}
            <table>
            {% for i in inp %}
              <tr>
                <th>{{ i.name }}</th>
                {% for a in i.args %}
                    <th>{{ a }}</th>
                {% endfor %}
              </tr>
            {% endfor %}
            </table>
        {% endif %}
        """)
        return tmp.render(inp=self.inp)

    def out(self):
        print("{point}: {description}\n {inp} {rpl}".format(rpl=self.parse_end(), inp=self.parse_inp(), point=self.point, description=self.description))

class ArgumentPass():
    def __init__(self, name, structure):
        self.name = name
        self.structure = structure

class ArgumentRaw():
    def __init__(self, desc):
        self.desc = desc
        self.raw = True

class URLArgument():
    def __init__(self, name, *args):
        self.name = name
        self.args = args

class Redirect(ArgumentRaw):
    def __init__(self, url):
        ArgumentRaw.__init__(self, url)
        self.raw = True

invoice_id = URLArgument("invoice_id", "The ID of the invoice you intend to view.")

Endpoint("/invoice/list", "List all invoices linked to your account.", invoices=ArgumentPass("invoice[]", structs["invoice"]))
Endpoint("/vps/list", "List all vServers linked to your account.", vpslist=ArgumentPass("vps[]", structs["vps"]))
Endpoint("/invoice/service_credit.json", "Display service credit associated with your account.", username=ArgumentRaw("Your username.", ), total=ArgumentPass("Your total service credit.", raw=True))
Endpoint("/invoice/{invoice_id}", "View information on a single Invoice.", inp=[invoice_id], invoice=ArgumentPass("invoice", structs["invoice"]))
Endpoint("/invoice/{invoice_id}.pdf", "View your invoice as a printable PDF file", inp=[invoice_id])
Endpoint("/invoice/{invoice_id}/resend", "Send an invoice e-mail to your e-mail address on file.", inp=[invoice_id], redirect=Redirect("/vps/list"))
