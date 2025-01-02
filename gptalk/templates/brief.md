## {{ citation }}

### Parties
{% for party in parties %}
- {{ party.name }} -- {{ party.role | join("-") }}
{%- endfor %}

{% if facts -%}
### Facts
{% for fact in facts %}
- {{ fact }}
{%- endfor %}
{%- endif %}

{% if prior_proceedings -%}
### Prior proceedings
{% for proceeding in prior_proceedings %}
- {{ proceeding }}
{%- endfor %}
{%- endif %}

### Issue

{{ issue }}

{% if rule -%}
### Rule

{{ rule }}
{%- endif %}

{% if application -%}
### Application

{{ application }}
{%- endif %}

### Conclusion

{{ conclusion }}
