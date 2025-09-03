from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django.utils.html import json_script
import json

class RepeatableChoiceWithOtherWidget(Select):
    """
    A custom widget that allows users to select from a list of choices
    and add an 'Other' option with a text input for custom entries.
    This widget supports repeatable fields, allowing users to add multiple
    selections with custom text inputs.
    """
    template_name = 'widgets/repeatable_choice_with_other.html'

    def __init__(self, attrs=None, choices=()):
        self._choices = list(choices)
        super().__init__(attrs, choices=self._choices)

    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f"""
            <div id="repeatable-{name}" class="repeatable-field"></div>
            {json_script(list(self.choices), f"{name}_choices")}
            <script>
            (function() {{
                const container = document.getElementById("repeatable-{name}");
                const choices = JSON.parse(document.getElementById("{name}_choices").textContent);
                let counter = 0;

                function createField(index) {{
                    const div = document.createElement('div');
                    const selectId = `id_{name}_${{index}}`;
                    const inputId = `id_{name}_other_${{index}}`;

                    let selectHTML = `<select name="{name}_${{index}}" id="${{selectId}}" class="form-control">
                        <option value="">-- Select --</option>`;
                    choices.forEach(([val, label]) => {{
                        selectHTML += `<option value="${{val}}">${{label}}</option>`;
                    }});
                    selectHTML += `<option value="other">Other</option></select>`;

                    const inputHTML = `<input type="text" name="{name}_other_${{index}}" id="${{inputId}}" 
                                        style="display:none;" class="form-control" 
                                        placeholder="Enter custom..." />`;

                    div.innerHTML = selectHTML + inputHTML;
                    container.appendChild(div);

                    const select = div.querySelector('select');
                    const input = div.querySelector('input');

                    select.addEventListener('change', () => {{
                        if (select.value === 'other') {{
                            input.style.display = 'inline-block';
                        }} else {{
                            input.style.display = 'none';
                        }}
                        createField(++counter);
                    }});
                }}

                createField(counter);
            }})();
            </script>
        """)