const FIELD_DEFINITIONS = [
  { key: 'genre', label: 'Genre', help: 'genre', source: 'genre', column: 'name' },
  { key: 'title', label: 'Title', help: 'title', source: 'sources', column: 'title' },
  { key: 'office', label: 'Office', help: 'office', source: 'office', column: 'name' },
  { key: 'siglum', label: 'Siglum', help: 'siglum', source: 'sources', column: 'siglum' },
  { key: 'feast', label: 'Feast', help: 'feast', source: 'feast', column: 'name' },
  { key: 'century', label: 'Century', help: 'century', source: 'sources', column: 'century' },
  { key: 'db', label: 'Source Database', help: 'db', source: 'db', column: 'shortcut' },
  { key: 'num_century', label: 'Numerical Century', help: 'num_century', source: 'sources', column: 'num_century' },
  { key: 'provenance', label: 'Provenance', help: 'provenance', source: 'sources', column: 'provenance' },
  { key: 'cursus', label: 'Cursus', help: 'cursus', source: 'sources', column: 'cursus' }
];

const DATA_FILES = {
  office: 'filter/static/filter/office.csv',
  genre: 'filter/static/filter/genre.csv',
  feast: 'filter/static/filter/feast.csv',
  db: 'filter/static/filter/db.csv',
  sources: 'filter/static/filter/sources.csv'
};

const TRANSLATE_KEY = {
  genre_incl: 'genre', office_incl: 'office', feast_incl: 'feast',
  db_incl: 'db', siglum_incl: 'siglum', title_incl: 'title',
  provenance_incl: 'provenance', century_incl: 'century',
  num_century_incl: 'num_century', cursus_incl: 'cursus',
  genre_excl: 'genre', office_excl: 'office', feast_excl: 'feast',
  db_excl: 'db', siglum_excl: 'siglum', title_excl: 'title',
  provenance_excl: 'provenance', century_excl: 'century',
  num_century_excl: 'num_century', cursus_excl: 'cursus'
};

function parseCsvLine(line) {
  const values = [];
  let value = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    if (char === '"') {
      if (inQuotes && line[i + 1] === '"') {
        value += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (char === ',' && !inQuotes) {
      values.push(value);
      value = '';
    } else {
      value += char;
    }
  }

  values.push(value);
  return values;
}

function parseCsv(text) {
  const lines = text.replace(/^\uFEFF/, '').split(/\r?\n/).filter((line) => line.trim() !== '');
  if (lines.length === 0) {
    return [];
  }

  const headers = parseCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const row = parseCsvLine(line);
    return headers.reduce((acc, header, index) => {
      acc[header] = row[index] ?? '';
      return acc;
    }, {});
  });
}

function uniqueSorted(values) {
  return [...new Set(values.filter((value) => value && value.trim() !== ''))].sort((a, b) => a.localeCompare(b));
}

async function loadChoices() {
  const datasets = await Promise.all(Object.entries(DATA_FILES).map(async ([key, path]) => {
    const fileUrl = new URL(path, document.baseURI);
    const response = await fetch(fileUrl);
    if (!response.ok) {
      throw new Error(`Unable to load ${path}`);
    }

    return [key, parseCsv(await response.text())];
  }));

  const dataByFile = Object.fromEntries(datasets);
  const choicesByField = {};

  FIELD_DEFINITIONS.forEach((field) => {
    const values = dataByFile[field.source].map((row) => String(row[field.column] ?? '')).map((v) => v.trim());
    choicesByField[field.key] = uniqueSorted(values);
  });

  return choicesByField;
}

function createSelect(name, index, choices) {
  const select = document.createElement('select');
  select.name = `${name}_${index}`;
  select.id = `id_${name}_${index}`;
  select.className = 'form-control';

  const empty = document.createElement('option');
  empty.value = '';
  empty.textContent = '-- Select --';
  select.appendChild(empty);

  choices.forEach((choice) => {
    const option = document.createElement('option');
    option.value = choice;
    option.textContent = choice;
    select.appendChild(option);
  });

  const other = document.createElement('option');
  other.value = 'other';
  other.textContent = 'Other';
  select.appendChild(other);

  return select;
}

function createRepeatableField(name, choices, container) {
  let counter = 0;

  function addField(index) {
    const wrapper = document.createElement('div');
    const select = createSelect(name, index, choices);
    const customInput = document.createElement('input');

    customInput.type = 'text';
    customInput.name = `${name}_other_${index}`;
    customInput.id = `id_${name}_other_${index}`;
    customInput.className = 'form-control mt-1';
    customInput.placeholder = 'Enter custom...';
    customInput.style.display = 'none';

    wrapper.appendChild(select);
    wrapper.appendChild(customInput);
    container.appendChild(wrapper);

    select.addEventListener('change', () => {
      customInput.style.display = select.value === 'other' ? 'inline-block' : 'none';
      counter += 1;
      addField(counter);
    });
  }

  addField(counter);
}

function collectDynamicField(name) {
  const values = [];
  let index = 0;

  while (document.querySelector(`[name="${name}_${index}"]`)) {
    const selected = document.querySelector(`[name="${name}_${index}"]`)?.value;
    if (selected === 'other') {
      const custom = document.querySelector(`[name="${name}_other_${index}"]`)?.value.trim();
      if (custom) {
        values.push(custom);
      }
    } else if (selected) {
      values.push(selected);
    }
    index += 1;
  }

  return [...new Set(values)];
}

function yamlScalar(value) {
  if (value === '') {
    return "''";
  }
  const simplePattern = /^[\p{L}\p{N}_ .\-/:()]+$/u;
  const reservedPattern = /^(true|false|null|~|yes|no|on|off|[-+]?\d+(\.\d+)?)$/i;
  if (simplePattern.test(value) && !reservedPattern.test(value)) {
    return value;
  }
  return `'${value.replace(/'/g, "''")}'`;
}

function serializeYaml(name, includeValues, excludeValues) {
  const lines = [`name: ${yamlScalar(name)}`];

  const appendBlock = (blockName, values) => {
    const entries = Object.entries(values);
    if (entries.length === 0) {
      lines.push(`${blockName}: {}`);
      return;
    }

    lines.push(`${blockName}:`);
    entries.forEach(([key, array]) => {
      lines.push(`  ${key}:`);
      array.forEach((item) => {
        lines.push(`  - ${yamlScalar(String(item))}`);
      });
    });
  };

  appendBlock('include_values', includeValues);
  appendBlock('exclude_values', excludeValues);

  return `${lines.join('\n')}\n`;
}

function buildSection(sectionId, sectionTitle, suffix, choicesByField) {
  const section = document.getElementById(sectionId);
  const title = document.createElement('h3');
  title.textContent = sectionTitle;
  section.appendChild(title);

  for (let i = 0; i < FIELD_DEFINITIONS.length; i += 2) {
    const row = document.createElement('div');
    row.className = 'row justify-content-around';

    [FIELD_DEFINITIONS[i], FIELD_DEFINITIONS[i + 1]].forEach((field, index) => {
      const col = document.createElement('div');
      col.className = index === 0 ? 'col md-3 mt-2' : 'col offset-md-1 mt-2';

      const key = `${field.key}_${suffix}`;
      col.innerHTML = `<b><label class="form-label">${field.label}</label></b> <a href="help.html#${field.help}" target="_blank" class="ms-1 text-decoration-none"><i class="bi bi-question-circle"></i></a>`;

      const container = document.createElement('div');
      container.id = `repeatable-${key}`;
      col.appendChild(container);

      createRepeatableField(key, choicesByField[field.key], container);
      row.appendChild(col);
    });

    section.appendChild(row);
  }
}

function initializeForm() {
  const form = document.getElementById('filtrationForm');
  if (!form) {
    return;
  }

  loadChoices().then((choicesByField) => {
    buildSection('include-section', 'Values to be included', 'incl', choicesByField);
    buildSection('exclude-section', 'Values to be exluded', 'excl', choicesByField);
  }).catch((error) => {
    const errorBox = document.getElementById('formLoadError');
    if (errorBox) {
      errorBox.textContent = `Unable to load filtering values: ${error.message}`;
      errorBox.style.display = 'block';
    }
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const nameInput = document.getElementById('id_name');
    const name = nameInput.value.trim();

    if (!name) {
      nameInput.setCustomValidity('Please fill out this field.');
      nameInput.reportValidity();
      return;
    }
    nameInput.setCustomValidity('');

    const formData = { name };
    FIELD_DEFINITIONS.forEach((field) => {
      formData[`${field.key}_incl`] = collectDynamicField(`${field.key}_incl`);
      formData[`${field.key}_excl`] = collectDynamicField(`${field.key}_excl`);
    });

    sessionStorage.setItem('filterFormData', JSON.stringify(formData));
    window.location.href = 'download.html';
  });
}

function downloadYaml(filename, content) {
  const blob = new Blob([content], { type: 'application/x-yaml;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${filename}.yaml`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function initializeDownloadPage() {
  const downloadButton = document.getElementById('downloadYamlButton');
  if (!downloadButton) {
    return;
  }

  const raw = sessionStorage.getItem('filterFormData');
  const errorBox = document.getElementById('downloadError');

  if (!raw) {
    errorBox.textContent = 'No form data found. Please create a filtration setup first.';
    errorBox.style.display = 'block';
    downloadButton.disabled = true;
    return;
  }

  const data = JSON.parse(raw);

  downloadButton.addEventListener('click', () => {
    const includeValues = {};
    const excludeValues = {};

    Object.keys(TRANSLATE_KEY).forEach((key) => {
      const value = data[key] || [];
      if (!Array.isArray(value) || value.length === 0) {
        return;
      }
      if (key.endsWith('_incl')) {
        includeValues[TRANSLATE_KEY[key]] = value;
      } else {
        excludeValues[TRANSLATE_KEY[key]] = value;
      }
    });

    const yaml = serializeYaml(data.name, includeValues, excludeValues);
    downloadYaml(data.name, yaml);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initializeForm();
  initializeDownloadPage();
});
