const form = document.querySelector('#brief-form');
const errors = document.querySelector('#form-errors');
const prefillStatus = document.querySelector('#prefill-status');
const statusMark = document.querySelector('.status-mark');
const success = document.querySelector('#success');

const labels = {
  purpose: {
    educate: 'Teach or explain',
    persuade: 'Persuade',
    recommend: 'Recommend a decision',
    sell: 'Sell or pitch',
    facilitate: 'Facilitate a session',
    celebrate: 'Celebrate or entertain',
  },
  archetype: {
    academic: 'Academic deck',
    executive: 'Executive deck',
    editorial: 'Editorial deck',
    workshop: 'Workshop deck',
    'playful-quiz': 'Playful quiz deck',
    'product-launch': 'Product launch deck',
    'data-analyst': 'Data analyst deck',
    custom: 'Custom deck',
  },
  medium: {
    'scientific-illustration': 'Scientific illustration',
    'editorial-photography': 'Editorial photography',
    'tactile-collage': 'Tactile collage',
    'paper-cut': 'Paper construction',
    painterly: 'Painterly scene',
    dimensional: 'Dimensional render',
    'data-led': 'Data-led visual',
    custom: 'Custom medium',
  },
  palette: {
    'mineral-ink': 'Mineral and ink',
    'forest-clay': 'Forest and clay',
    'oxblood-paper': 'Oxblood and paper',
    monochrome: 'Tonal monochrome',
    'sunlit-primary': 'Sunlit primary',
    custom: 'Custom palette',
  },
  typography: {
    'scholarly-humanist': 'Scholarly humanist',
    editorial: 'Editorial',
    executive: 'Executive',
    expressive: 'Expressive',
    technical: 'Technical',
    custom: 'Custom typography',
  },
};

const fields = {
  title: document.querySelector('#title'),
  topic: document.querySelector('#topic'),
  content: document.querySelector('#content'),
  audience: document.querySelector('#audience'),
  purpose: document.querySelector('#purpose'),
  outcome: document.querySelector('#audience-outcome'),
  presenter: document.querySelector('#presenter'),
  language: document.querySelector('#language'),
  context: document.querySelector('#context'),
  slideCount: document.querySelector('#slide-count'),
  duration: document.querySelector('#duration'),
  aspect: document.querySelector('#aspect-ratio'),
  notes: document.querySelector('#speaker-notes'),
  citations: document.querySelector('#citations'),
  outputName: document.querySelector('#output-name'),
  density: document.querySelector('#density'),
  medium: document.querySelector('#visual-medium'),
  palette: document.querySelector('#palette'),
  typography: document.querySelector('#typography'),
  energy: document.querySelector('#energy'),
  imagery: document.querySelector('#imagery-frequency'),
  research: document.querySelector('#research'),
  customDirection: document.querySelector('#custom-direction'),
  referenceDeck: document.querySelector('#reference-deck'),
  brandAssetPaths: document.querySelector('#brand-asset-paths'),
  sourceFilePaths: document.querySelector('#source-file-paths'),
};

const proof = {
  canvas: document.querySelector('#proof-canvas'),
  slide: document.querySelector('#slide-proof'),
  archetype: document.querySelector('#proof-archetype'),
  title: document.querySelector('#proof-title'),
  audience: document.querySelector('#proof-audience'),
  medium: document.querySelector('#proof-medium'),
  count: document.querySelector('#proof-count'),
  purpose: document.querySelector('#proof-purpose'),
  outcome: document.querySelector('#proof-outcome'),
  style: document.querySelector('#proof-style'),
  type: document.querySelector('#proof-type'),
};

function setValue(element, value) {
  if (value === undefined || value === null) return 0;
  if (element.type === 'checkbox') {
    element.checked = Boolean(value);
  } else {
    element.value = String(value);
  }
  return String(value).trim() ? 1 : 0;
}

function setRadio(name, value) {
  if (!value) return 0;
  const radio = document.querySelector(`input[name="${name}"][value="${CSS.escape(value)}"]`);
  if (!radio) return 0;
  radio.checked = true;
  return 1;
}

function applyPrefill(data) {
  const project = data.project || {};
  const delivery = data.delivery || {};
  const style = data.style || {};
  const assets = data.assets || {};
  const policy = data.content_policy || {};
  let count = 0;

  count += setValue(fields.title, project.title);
  count += setValue(fields.topic, project.topic);
  count += setValue(fields.content, project.content);
  count += setValue(fields.audience, project.audience);
  count += setValue(fields.purpose, project.purpose);
  count += setValue(fields.outcome, project.audience_outcome);
  count += setValue(fields.presenter, project.presenter);
  count += setValue(fields.language, project.language);
  count += setValue(fields.context, project.context);
  count += setValue(fields.slideCount, delivery.slide_count);
  count += setValue(fields.duration, delivery.duration_minutes);
  count += setValue(fields.aspect, delivery.aspect_ratio);
  count += setValue(fields.notes, delivery.speaker_notes);
  count += setValue(fields.citations, delivery.citations);
  count += setValue(fields.outputName, delivery.output_name);
  count += setRadio('archetype', style.archetype);
  count += setValue(fields.density, style.density);
  count += setValue(fields.medium, style.visual_medium);
  count += setValue(fields.palette, style.palette);
  count += setValue(fields.typography, style.typography);
  count += setValue(fields.energy, style.energy);
  count += setValue(fields.imagery, style.imagery_frequency);
  count += setValue(fields.customDirection, style.custom_direction);
  count += setValue(fields.referenceDeck, assets.reference_deck);
  count += setValue(fields.brandAssetPaths, (assets.brand_assets || []).join('\n'));
  count += setValue(fields.sourceFilePaths, (assets.source_files || []).join('\n'));
  count += setValue(fields.research, policy.research);

  prefillStatus.textContent = count > 0 ? `${count} answers recovered from your prompt` : 'Ready for your brief';
  statusMark.classList.add('ready');
  updateProof();
}

function selectedArchetype() {
  return document.querySelector('input[name="archetype"]:checked')?.value || 'editorial';
}

function updateProof() {
  const archetype = selectedArchetype();
  const ratio = fields.aspect.value;
  const title = fields.title.value.trim() || 'Your presentation title';
  const audience = fields.audience.value.trim();
  const outcome = fields.outcome.value.trim();
  const count = Number(fields.slideCount.value || 0);

  proof.canvas.textContent = ratio;
  proof.slide.style.aspectRatio = ratio === '4:3' ? '4 / 3' : '16 / 9';
  proof.archetype.textContent = labels.archetype[archetype] || labels.archetype.custom;
  proof.title.textContent = title;
  proof.audience.textContent = audience ? `Prepared for ${audience}` : 'Prepared for your audience';
  proof.medium.textContent = labels.medium[fields.medium.value] || fields.medium.value;
  proof.count.textContent = `${count || 0} ${count === 1 ? 'slide' : 'slides'}`;
  proof.purpose.textContent = labels.purpose[fields.purpose.value] || fields.purpose.value;
  proof.outcome.textContent = outcome || 'Not set yet';
  proof.style.textContent = `${labels.palette[fields.palette.value] || fields.palette.value}, ${fields.energy.value}`;
  proof.type.textContent = labels.typography[fields.typography.value] || fields.typography.value;

  const themes = {
    academic: ['#e1e6dc', '#17231a'],
    executive: ['#d8d1c8', '#251913'],
    editorial: ['#dce7d7', '#1d231e'],
    workshop: ['#e8dfca', '#2b241b'],
    'playful-quiz': ['#efd75b', '#2b291e'],
    'product-launch': ['#c9d5c1', '#14241b'],
    'data-analyst': ['#cddcd4', '#163329'],
    custom: ['#e0e1d5', '#20231f'],
  };
  const [background, color] = themes[archetype];
  proof.slide.style.backgroundColor = background;
  proof.slide.style.color = color;
}

function lines(value) {
  return value.split('\n').map((item) => item.trim()).filter(Boolean);
}

function buildBrief() {
  const brandAssets = lines(fields.brandAssetPaths.value);
  const sourceFiles = lines(fields.sourceFilePaths.value);
  return {
    schema_version: 1,
    project: {
      title: fields.title.value,
      topic: fields.topic.value,
      content: fields.content.value,
      audience: fields.audience.value,
      purpose: fields.purpose.value,
      audience_outcome: fields.outcome.value,
      language: fields.language.value,
      presenter: fields.presenter.value,
      context: fields.context.value,
    },
    delivery: {
      slide_count: Number(fields.slideCount.value),
      duration_minutes: Number(fields.duration.value),
      aspect_ratio: fields.aspect.value,
      speaker_notes: fields.notes.checked,
      citations: fields.citations.value,
      output_name: fields.outputName.value,
    },
    style: {
      archetype: selectedArchetype(),
      energy: fields.energy.value,
      visual_medium: fields.medium.value,
      palette: fields.palette.value,
      typography: fields.typography.value,
      density: fields.density.value,
      imagery_frequency: fields.imagery.value,
      custom_direction: fields.customDirection.value,
      reference_notes: '',
    },
    assets: {
      reference_deck: fields.referenceDeck.value,
      brand_assets: brandAssets,
      source_files: sourceFiles,
    },
    content_policy: {
      research: fields.research.value,
      factuality: 'source-required',
      visuals: 'imagegen-raster-only',
      allow_svg: false,
    },
  };
}

function validate() {
  const required = [fields.title, fields.topic, fields.content, fields.audience, fields.outcome];
  const missing = [];
  required.forEach((field) => {
    const empty = !field.value.trim();
    field.setAttribute('aria-invalid', String(empty));
    if (empty) missing.push(field.closest('label').querySelector('span').textContent);
  });
  if (Number(fields.slideCount.value) < 3 || Number(fields.slideCount.value) > 60) missing.push('Slides must be between 3 and 60');
  if (Number(fields.duration.value) < 1 || Number(fields.duration.value) > 240) missing.push('Minutes must be between 1 and 240');
  return missing;
}

form.addEventListener('input', updateProof);
form.addEventListener('change', updateProof);

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errors.replaceChildren();
  const missing = validate();
  if (missing.length) {
    const list = document.createElement('ul');
    missing.forEach((message) => {
      const item = document.createElement('li');
      item.textContent = message;
      list.appendChild(item);
    });
    errors.appendChild(list);
    document.querySelector('[aria-invalid="true"]')?.focus();
    return;
  }

  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  button.querySelector('span:first-child').textContent = 'Locking brief';
  try {
    const response = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(buildBrief()),
    });
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error((result.errors || ['Could not save the brief']).join(' '));
    success.hidden = false;
    success.querySelector('h2').focus();
  } catch (error) {
    errors.textContent = error.message;
    button.disabled = false;
    button.querySelector('span:first-child').textContent = 'Lock brief and continue';
  }
});

fetch('/api/prefill')
  .then((response) => {
    if (!response.ok) throw new Error('Could not load the prompt prefill');
    return response.json();
  })
  .then(applyPrefill)
  .catch((error) => {
    prefillStatus.textContent = error.message;
    statusMark.classList.add('ready');
    updateProof();
  });
