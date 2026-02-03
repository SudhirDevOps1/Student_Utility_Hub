# 🎓 Student Utility Hub - JSON Customization Guide

## 📁 JSON Configuration Files

All customizable data is stored in the `data/` folder as JSON files. You can edit these files to customize formulas, periodic table, quotes, and translations **without touching any code**!

---

## 📚 Available JSON Files

### 1. **formulas.json** - Formula Sheet Customization

**Location:** `data/formulas.json`

**Structure:**
```json
{
  "mathematics": {
    "algebra": [
      {"formula": "LaTeX formula", "name": "Formula Name"}
    ]
  },
  "physics": {
    "mechanics": [...]
  },
  "chemistry": {
    "basic": [...]
  }
}
```

**How to Add/Edit:**
- Add new categories under `mathematics`, `physics`, or `chemistry`
- Add new formulas to existing categories
- Use LaTeX syntax for formulas (e.g., `\\frac{a}{b}` for fractions)
- Give each formula a descriptive name

**Example - Adding a New Formula:**
```json
{
  "formula": "E = mc^2",
  "name": "Mass-Energy Equivalence"
}
```

---

### 2. **periodic_table.json** - Periodic Table Elements

**Location:** `data/periodic_table.json`

**Structure:**
```json
{
  "elements": [
    {
      "name": "Hydrogen",
      "symbol": "H",
      "number": 1,
      "mass": "1.008",
      "category": "Nonmetal",
      "group": 1
    }
  ]
}
```

**How to Add Elements:**
- Add new element objects to the `elements` array
- Include: name, symbol, atomic number, mass, category, group
- Categories: Nonmetal, Noble Gas, Alkali Metal, Transition Metal, etc.

---

### 3. **quotes.json** - Motivational Quotes

**Location:** `data/quotes.json`

**Structure:**
```json
{
  "quotes": [
    "Quote text - Author Name",
    "Another quote - Author"
  ]
}
```

**How to Add Quotes:**
- Simply add new quote strings to the `quotes` array
- Format: "Quote text - Author Name"
- These appear in the **Focus Mode** feature

---

### 4. **translations.json** - Common Phrase Translations

**Location:** `data/translations.json`

**Structure:**
```json
{
  "common_phrases": {
    "Hello": {
      "Hindi": "नमस्ते",
      "Spanish": "Hola",
      "French": "Bonjour",
      "German": "Hallo"
    }
  }
}
```

**How to Add Translations:**
- Add new phrases under `common_phrases`
- Add new languages to existing phrases
- Use Unicode for non-English characters

---

## 🔧 How to Customize

### Step 1: Locate the JSON File
Navigate to: `student_app/data/`

### Step 2: Edit with Any Text Editor
- Notepad, VS Code, or any text editor
- **IMPORTANT:** Maintain valid JSON syntax
- Use tools like jsonlint.com to validate

### Step 3: Save & Refresh
- Save your changes
- Refresh the Streamlit app
- Changes appear immediately!

---

## ✅ JSON Syntax Tips

1. **Use Double Quotes:** `"key": "value"` (not single quotes)
2. **No Trailing Commas:** Last item should not have a comma
3. **Escape Special Characters:** Use `\\` for LaTeX
4. **UTF-8 Encoding:** For non-English characters

### Valid Example:
```json
{
  "quotes": [
    "First quote",
    "Second quote"
  ]
}
```

### Invalid Example (trailing comma):
```json
{
  "quotes": [
    "First quote",
    "Second quote",  ← Remove this comma!
  ]
}
```

---

## 🎯 Quick Customization Examples

### Add a New Math Formula:
Open `data/formulas.json`, find the `mathematics` section, and add:
```json
{
  "formula": "\\sin^2(x) + \\cos^2(x) = 1",
  "name": "Pythagorean Identity"
}
```

### Add a Motivational Quote:
Open `data/quotes.json` and add:
```json
"Your new quote here - Your Name"
```

### Add a Chemical Element:
Open `data/periodic_table.json` and add to `elements`:
```json
{
  "name": "Uranium",
  "symbol": "U",
  "number": 92,
  "mass": "238.03",
  "category": "Actinide",
  "group": 3
}
```

---

## 🚀 Benefits of JSON Customization

✅ No coding required
✅ Easy to share custom configurations
✅ Version control friendly
✅ Backup and restore easily
✅ Add unlimited formulas, quotes, elements
✅ Multilingual support

---

## 📞 Need Help?

If your JSON file is not loading:
1. Check for syntax errors (use jsonlint.com)
2. Ensure file is saved in `data/` folder
3. Check file encoding is UTF-8
4. Restart the Streamlit app

---

**Built by Sudhir Kumar | @SudhirDevOps1**
