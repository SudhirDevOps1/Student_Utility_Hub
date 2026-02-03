import streamlit as st
import requests
import json_utils

def show():
    st.markdown("## 🌐 Utility Features")
    
    tabs = st.tabs(["Unit Converter", "Periodic Table", "Dictionary", "Translator"])
    
    # Unit Converter
    with tabs[0]:
        st.markdown("### 🔄 Unit Converter")
        
        conversion_type = st.selectbox("Conversion Type", 
                                      ["Length", "Weight", "Temperature", "Time", "Speed"])
        
        if conversion_type == "Length":
            col1, col2 = st.columns(2)
            with col1:
                value = st.number_input("Value", 0.0, 1000000.0, 1.0)
                from_unit = st.selectbox("From", ["Meters", "Kilometers", "Miles", "Feet", "Inches", "Centimeters"])
            
            with col2:
                to_unit = st.selectbox("To", ["Meters", "Kilometers", "Miles", "Feet", "Inches", "Centimeters"])
            
            # Conversion factors to meters
            to_meters = {
                "Meters": 1, "Kilometers": 1000, "Miles": 1609.34,
                "Feet": 0.3048, "Inches": 0.0254, "Centimeters": 0.01
            }
            
            result = value * to_meters[from_unit] / to_meters[to_unit]
            st.success(f"### {value} {from_unit} = {result:.4f} {to_unit}")
        
        elif conversion_type == "Weight":
            col1, col2 = st.columns(2)
            with col1:
                value = st.number_input("Value", 0.0, 1000000.0, 1.0)
                from_unit = st.selectbox("From", ["Kilograms", "Grams", "Pounds", "Ounces", "Tons"])
            
            with col2:
                to_unit = st.selectbox("To", ["Kilograms", "Grams", "Pounds", "Ounces", "Tons"])
            
            to_kg = {
                "Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592,
                "Ounces": 0.0283495, "Tons": 1000
            }
            
            result = value * to_kg[from_unit] / to_kg[to_unit]
            st.success(f"### {value} {from_unit} = {result:.4f} {to_unit}")
        
        elif conversion_type == "Temperature":
            col1, col2 = st.columns(2)
            with col1:
                value = st.number_input("Value", -273.0, 10000.0, 25.0)
                from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
            
            with col2:
                to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
            
            # Convert to Celsius first
            if from_unit == "Fahrenheit":
                celsius = (value - 32) * 5/9
            elif from_unit == "Kelvin":
                celsius = value - 273.15
            else:
                celsius = value
            
           # Convert from Celsius to target
            if to_unit == "Fahrenheit":
                result = celsius * 9/5 + 32
            elif to_unit == "Kelvin":
                result = celsius + 273.15
            else:
                result = celsius
            
            st.success(f"### {value}° {from_unit} = {result:.2f}° {to_unit}")
        
        elif conversion_type == "Time":
            col1, col2 = st.columns(2)
            with col1:
                value = st.number_input("Value", 0.0, 1000000.0, 1.0)
                from_unit = st.selectbox("From", ["Seconds", "Minutes", "Hours", "Days", "Weeks"])
            
            with col2:
                to_unit = st.selectbox("To", ["Seconds", "Minutes", "Hours", "Days", "Weeks"])
            
            to_seconds = {
                "Seconds": 1, "Minutes": 60, "Hours": 3600,
                "Days": 86400, "Weeks": 604800
            }
            
            result = value * to_seconds[from_unit] / to_seconds[to_unit]
            st.success(f"### {value} {from_unit} = {result:.4f} {to_unit}")
        
        else:  # Speed
            col1, col2 = st.columns(2)
            with col1:
                value = st.number_input("Value", 0.0, 100000.0, 100.0)
                from_unit = st.selectbox("From", ["m/s", "km/h", "mph"])
            
            with col2:
                to_unit = st.selectbox("To", ["m/s", "km/h", "mph"])
            
            to_ms = {"m/s": 1, "km/h": 0.277778, "mph": 0.44704}
            
            result = value * to_ms[from_unit] / to_ms[to_unit]
            st.success(f"### {value} {from_unit} = {result:.2f} {to_unit}")
    
    # Periodic Table
    with tabs[1]:
        st.markdown("### ⚛️ Periodic Table Reference")
        
        element_search = st.text_input("Search Element", "Hydrogen")
        
        # Load periodic table from JSON
        periodic_data = json_utils.load_json_data('periodic_table.json')
        elements = {}
        
        for elem in periodic_data.get('elements', []):
            elements[elem['name']] = {
                "symbol": elem['symbol'],
                "number": elem['number'],
                "mass": elem['mass'],
                "category": elem['category']
            }
        
        if element_search in elements:
            elem = elements[element_search]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Symbol", elem["symbol"])
            with col2:
                st.metric("Atomic Number", elem["number"])
            with col3:
                st.metric("Atomic Mass", elem["mass"])
            with col4:
                st.write(f"**Category**\n{elem['category']}")
        else:
            st.warning("Element not found in database")
        
        st.markdown("---")
        st.markdown("### 📚 Common Elements")
        for name, data in list(elements.items())[:8]:
            st.write(f"**{data['number']}. {name} ({data['symbol']})** - {data['mass']} u")
    
    # Dictionary
    with tabs[2]:
        st.markdown("### 📖 Dictionary & Thesaurus")
        
        word = st.text_input("Enter a word", "serendipity")
        
        if st.button("🔍 Look Up"):
            dict_data = json_utils.load_json_data('dictionary.json')
            words = dict_data.get('words', {})
            
            if word.lower() in words:
                word_info = words[word.lower()]
                
                st.markdown(f"### {word.title()}")
                st.markdown(f"*{word_info['part_of_speech']}*")
                
                st.markdown("**Definition:**")
                st.info(word_info['definition'])
                
                st.markdown("**Example:**")
                st.write(f"*\"{word_info['example']}\"*")
                
                if word_info.get('synonyms'):
                    st.markdown("**Synonyms:**")
                    st.write(", ".join(word_info['synonyms']))
            else:
                st.warning(f"Word '{word}' not found in dictionary. Add it to dictionary.json!")
        
        st.markdown("---")
        st.markdown("### 📝 Word of the Day")
        
        dict_data = json_utils.load_json_data('dictionary.json')
        wotd= dict_data.get('word_of_the_day', {})
        
        if wotd:
            st.markdown(f"**{wotd['word']}**")
            st.write(f"*{wotd['part_of_speech']}*: {wotd['definition']}")
            if wotd.get('example'):
                st.caption(f"Example: {wotd['example']}")
    
    # Translator
    with tabs[3]:
        st.markdown("### 🌍 Language Translator")
        
        st.info("Simple text translation tool")
        
        col1, col2 = st.columns(2)
        with col1:
            from_lang = st.selectbox("From Language", ["English", "Hindi", "Spanish", "French", "German"])
        with col2:
            to_lang = st.selectbox("To Language", ["Hindi", "English", "Spanish", "French", "German"])
        
        text_to_translate = st.text_area("Enter text to translate", height=150)
        
        if st.button("🔄 Translate"):
            st.info("Note: Full translation requires API integration (Google Translate API)")
            st.markdown("### Translated Text:")
            st.write("Translation would appear here with API integration")
        
        st.markdown("---")
        st.markdown("### 🗣️ Common Phrases")
        
        # Load translations from JSON
        translations_data = json_utils.load_json_data('translations.json')
        phrases = translations_data.get('common_phrases', {})
        
        for english, translations in phrases.items():
            st.write(f"**{english}:** {translations.get(to_lang, 'N/A')}")
