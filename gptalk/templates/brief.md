## {{ citation }}

### Parties
{% for party in parties %}
- {{ party.name }} -- {{ party.role | join("-") }}
{%- endfor %}

### Facts
{% for fact in facts %}
- {{ fact }}
{%- endfor %}

### Prior proceedings
{% for proceeding in prior_proceedings %}
- {{ proceeding }}
{%- endfor %}

### Issue

{{ issue }}

### Rule

{{ rule }}

### Application

{{ application }}

### Conclusion

{{ conclusion }}
