import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import difflib
import speech_recognition as sr

# Define your dataset and other variables here...
dataset = [
    
    (["About"], "About Page👋", None),
    (["Demo"], "Demo Page👋", None),
    (["Health Tips"], "Health Tips Page👋", None),
    (["Advance Chatting"], "Advance Chatting Page👋", None),
    # (["fever"], "Apply a cold compress and take fever-reducing medication like paracetamol.", None),
    # (["headache"], "Biogesic 😘😘😘", "z-img/saridon.png"),
    (["hospital", "nearest hospital"], "You can search for nearby hospitals using online maps or call emergency services for assistance. The nearest hospital in your location is Doctors Hospital.", "z-img/spc-doctors.jpg"),
    (["COVID-19", "symptoms of COVID-19"], "Common symptoms include fever, cough, and difficulty breathing. If you suspect you have COVID-19, seek medical advice immediately.", None),
    (["common cold", "prevent the common cold"], "Wash your hands frequently, avoid close contact with sick individuals, and maintain a healthy lifestyle with a balanced diet and regular exercise.", None),
    (["sprained ankle", "ice for a sprained ankle"], "Apply ice to the affected area and elevate it to reduce swelling. Rest and avoid putting weight on the ankle.", "z-img/sprained-ankle.jpg"),
    (["prevent COVID-19", "prevention measures for COVID-19"], "To prevent COVID-19, practice good hygiene by washing your hands frequently, wearing masks in public places, practicing social distancing, and getting vaccinated when available.", None),
    (["updates COVID-19", "status or update for COVID-19"], "For the latest updates on COVID-19, refer to reliable sources such as the World Health Organization (WHO) or your local health department.", None),
    (["What is MICA?"], "I am MICA or Medical Information Chat Assistant. I assist users with healthcare-related inquiries and provide valuable information and assistance.", "MICA-dila.png"),
    (["Hi"], "Hello! How can I help you?👋", "z-img/MICA_hello.png"),
    (["Hello"], "Hello! How can I help you?👋", "z-img/MICA_hello.png"),
    
    # SYMPTOMS SECTION
    # (["KEYWORD"], "RESPONSE", "IMG (OPTIONAL)"),
    (["cough", "coughing"], "Stay hydrated, use cough drops or lozenges, try over-the-counter cough medicines such as Solmux or Bactidol, and consider using a humidifier to moisten the air.", "z-img/medicine/bactidol.jpg", ["Bactidol", "Solmux", "Myracof", "Robitussin"]),
    (["nasal congestion", "nasal", "congestion"], "Use saline nasal sprays or rinses, try over-the-counter decongestants such as Sinutab or Decolgen, use a humidifier, and consider taking a hot shower to help relieve congestion.", "z-img/medicine/sinutab.jpg", ["Sinutab", "Decolgen", "Nafarin-A"]),
    (["sore throat", "throat", "sore", "hoarseness", "hoarse"], "Gargle with warm salt water, drink warm liquids such as tea with honey, use throat lozenges such as Strepsils or Cepacol, and consider over-the-counter pain relievers like acetaminophen or ibuprofen.", "z-img/medicine/strepsils.jpg", ["Cepacol", "Diflam Forte", "Strepsils"]),
    (["runny nose", "runny", "drippy"], "Use over-the-counter antihistamines or decongestants such as Neozep, stay hydrated, and consider using a humidifier.", "z-img/medicine/neozep.jpg", ["Neozep", "Sinutab"]),
    (["sneezing", "sneeze", "sneezy"], "Avoid triggers if possible (such as allergens), use over-the-counter antihistamines such as Benadryl or Cetirizine, and consider using nasal corticosteroid sprays.", "z-img/medicine/cetirizine.png", ["Benadryl", "Cetirizine", "Neozep", "Decolgen"]),
    (["headache", "head", "migraine", "head ache"], "Rest in a quiet, dark room, apply a cold compress to the forehead, try over-the-counter pain relievers like saridon or ibuprofen, and stay hydrated.", "z-img/medicine/saridon.png", ["Saridon", "Biogesic", "Rexidol Forte"]),
    (["fatigue", "tired", "unrest"], "Get plenty of rest, maintain a regular sleep schedule, engage in light physical activity, eat a balanced diet, and stay hydrated. For faster relief, consider using over-the-counter medicines such as Genexa.", "z-img/medicine/genexa.png", ["Genexa"]),
    (["fever", "high temp", "high temperature", "feverish", "hot"], "Drink plenty of fluids, rest, dress lightly, use over-the-counter fever reducers like Paracetamol or Ibuprofen, and seek medical attention if the fever persists or is high.", "z-img/medicine/biogesic.jpg", ["Biogesic", "Ibuprofen", "Calpol"]),
    (["loss of appetite", "appetite"], "Eat small, frequent meals, choose foods that are easy to digest, stay hydrated, and try to increase calorie intake with nutritious snacks.", None, [""]),
    
    (["dizzy", "dizziness", "collapse", "fall"], "Sit or lie down, stay hydrated, avoid sudden movements, and consider deep breathing exercises or relaxation techniques. For faster relief, consider taking medications such as Dizitab or Bonamine complemented by breathing exercises.", "z-img/medicine/dizitab.png", ["Dizitab", "Bonamine"]),
    (["shortness of breath", "shortness", "breath"], "Sit upright, practice breathing exercises, use a fan or open windows for fresh air. For faster relief, consider taking over-the-counter medications such as Asmalin complemented by use of inhaler. Seek medical attention if the shortness of breath is severe or persistent.", "z-img/medicine/asmalin.jpg", ["Asmalin"]),
    (["nosebleed", "nose bleed"], "Lean forward slightly and pinch the nostrils together for several minutes, apply an ice pack to the bridge of the nose, and avoid blowing your nose or picking at it.", None, [""]),
    (["nausea", "nauseous", "vomiting", "vomit", "puke", "puking"], "Stay hydrated with clear fluids, eat small, bland meals, avoid strong odors or foods that trigger nausea, and consider over-the-counter anti-nausea medications such as Dizitab.", "z-img/medicine/dizitab.png", ["Dizitab", "Bonamine"]),
    (["blurry", "blur", "blurry vision", "blurriness", "double vision", "vision", "cloudy", "see"], "Visit an eye doctor for an eye exam, especially if it's a sudden or persistent issue. Rest your eyes periodically, especially if you spend long hours in front of screens. Ensure proper lighting when reading or using electronic devices.", None, [""]),
    (["irregular heartbeat", "irregular", "heartbeat", "heart beat", "beat"], "Seek medical attention if you experience irregular heartbeats frequently or if they are accompanied by chest pain, dizziness, or shortness of breath. Maintain a healthy lifestyle with regular exercise and a balanced diet. Manage stress levels through relaxation techniques like deep breathing or meditation.", None, [""]),
    (["dehydration", "dry skin", "dry mouth", "dry lip", "chapped lip", "lips are chapped"], "Drink plenty of fluids, especially water, to stay hydrated. Use moisturizers for dry skin and lip balm for dry lips. Avoid caffeine and alcohol, as they can contribute to dehydration.", None, [""]),
    (["stiff neck", "stiff", "neck"], "Apply heat or cold packs to the affected area. Practice gentle neck stretches and exercises. Maintain good posture and avoid activities that strain the neck muscles. For faster pain relief, consider using medications such as Muskelax.", "z-img/medicine/muskelax.png", ["Muskelax"]),
    (["hunger", "extreme hunger", "hungry"], "Eat regular, balanced meals and snacks throughout the day to maintain stable blood sugar levels. Include protein, fiber, and healthy fats in your meals to promote satiety. Avoid skipping meals, as it can lead to excessive hunger and overeating later.", None, [""]),
    
    (["numbness", "tingling", "sensation", "numb"], "Rest the affected limb or area. Massage the area gently to improve blood circulation. Avoid activities that exacerbate the numbness or tingling.", None, [""]),
    (["weight loss", "loss of weight", "lose weight", "lose", "losing weight", "losing"], "Ensure you're eating enough calories to maintain a healthy weight. Eat nutrient-dense foods and consider consulting a dietitian for personalized meal planning. Rule out underlying medical conditions causing unintentional weight loss by consulting a healthcare professional.", None, [""]),
    (["irritation", "irritability", "irritated"], "Practice stress management techniques such as deep breathing, meditation, or yoga. Communicate openly about your feelings and needs with loved ones or a therapist. Ensure you're getting enough quality sleep to help regulate mood.", None, [""]),
    (["weakness", "weak", "frail"], "Engage in regular physical activity to improve strength and endurance. Eat a balanced diet rich in protein, vitamins, and minerals to support muscle health. Consider incorporating resistance training exercises into your fitness routine.", None, [""]),
    (["heartburn", "heartburn", "indigestion", "heart", "burning"], "Avoid trigger foods and beverages that exacerbate heartburn, such as spicy or fatty foods, caffeine, and alcohol. Eat smaller, more frequent meals and avoid lying down immediately after eating. Over-the-counter antacids or acid reducers may provide relief; consult a healthcare professional if symptoms persist.", "z-img/medicine/kremil-s.png", ["Kremil-S", "Gaviscon"]),
    (["anxiety", "panic", "panicking"], "Practice relaxation techniques such as deep breathing, progressive muscle relaxation, or mindfulness meditation. Seek support from a therapist or counselor to address underlying causes of anxiety. Consider medication or other treatments as recommended by a mental health professional.", None, [""]),
    (["snoring", "snore"], "Maintain a healthy weight and avoid alcohol or sedatives before bedtime, as they can relax throat muscles and contribute to snoring. Sleep on your side rather than your back to reduce snoring. Consider using nasal strips or a continuous positive airway pressure (CPAP) machine if snoring persists.", None, [""]),
    (["loss of consciousness", "consciousness"], "Seek immediate medical attention if you or someone else experiences loss of consciousness. Ensure a safe environment to prevent injury during episodes of loss of consciousness. Follow any medical recommendations or treatment plans provided by healthcare professionals.", None, [""]),
    (["seizure"], "Stay with the person experiencing the seizure and ensure their safety by removing nearby objects. Protect the person's head from injury by placing something soft under it. After the seizure, keep the person comfortable and monitor their breathing; seek medical attention if it's their first seizure or if it lasts longer than usual.", None, [""]),
    (["difficulty swallowing", "difficult swallowing", "swallowing", "swallow"], "Stay hydrated with small sips of water between bites, eat softer foods that are easier to swallow, take smaller bites and chew thoroughly, avoid eating quickly or talking while eating, consider swallowing therapy exercises recommended by a speech therapist, consult a healthcare professional if difficulty swallowing persists or worsens.", None, [""]),
    
    (["wheezing", "wheeze"], "Eat slowly and chew food thoroughly. Stay hydrated by drinking plenty of fluids, especially while eating. Avoid large bites of food and foods that are difficult to swallow; consult a healthcare professional if swallowing difficulties persist.", None, [""]),
    (["diarrhea", "lbm", "poop", "feces", "constipation", "irregular bowel movement", "bowel movement", "bowel"], "Stay hydrated with clear fluids, eat a balanced diet including foods like bananas, rice, applesauce, and toast (BRAT diet), avoid caffeine, dairy, spicy foods, and high-fiber foods, consider over-the-counter medications like loperamide for diarrhea or stool softeners for constipation.", "z-img/medicine/diatabs.png", ["Diatabs", "Imodium", "Loperamide HCI"]),
    (["lightheaded", "light", "headed"], "Sit or lie down to avoid falling, drink water or other clear fluids to stay hydrated, avoid sudden movements or standing up too quickly, if prone to lightheadedness, consider eating small, frequent meals to maintain blood sugar levels.", None, [""]),
    (["memory", "concentrate", "concentrating"], "Practice mental exercises like puzzles or memory games, establish a regular sleep schedule and ensure adequate sleep, maintain a balanced diet rich in nutrients that support brain health, such as omega-3 fatty acids, minimize distractions and create a conducive environment for concentration. In conjuction with these, consider taking supplements such as Memo Plus Gold.", "z-img/medicine/memo-plus.jpg", ["Memo Plus Gold", "Solemax Memory"]),
    (["itchy", "itchiness", "rash", "skin rash", "inflammation", "inflamed", "redness", "skin"], "Apply cold compresses or calamine lotion to soothe itching, take lukewarm baths with colloidal oatmeal or baking soda, avoid scratching to prevent further irritation or infection, use fragrance-free, gentle skincare products and detergents. For faster relief, consider using a itch relief cream. consult a dermatologist for persistent or severe symptoms.", "z-img/medicine/bepanthen.jpg"),
    (["swell", "swelling"], "Elevate the affected area above heart level to reduce swelling, apply cold compresses or ice packs to constrict blood vessels, avoid salty foods and excessive sodium intake, wear compression stockings or garments if recommended by a healthcare professional.", None, [""]),
    (["bloating", "bloat"], "Eat smaller, more frequent meals, avoid gas-producing foods like beans, cabbage, and carbonated drinks, chew food slowly and thoroughly to aid digestion, stay hydrated and incorporate fiber-rich foods into your diet gradually, consider over-the-counter medications like simethicone for gas relief.", None, [""]),
    (["frequent urination", "urination", "urinate", "frequently"], "Limit fluid intake before bedtime, avoid caffeine and alcohol, which can irritate the bladder, practice bladder training techniques to gradually increase the time between bathroom trips, consult a healthcare professional if frequent urination is accompanied by pain or other symptoms.", None, [""]),
    (["blood in urine", "urine blood", "bloody urine"], "Seek medical attention promptly to determine the underlying cause, increase fluid intake to dilute urine and reduce irritation, avoid strenuous physical activity that may exacerbate bleeding, refrain from taking nonsteroidal anti-inflammatory drugs (NSAIDs) that can thin the blood. For faster relief, consider taking medications such as Ciprofloxacin.", "z-img/medicine/ciprofloxacin.png", ["Ciprofloxacin"]),
    (["allergy", "allergies"], "Identify and avoid triggers, such as pollen, dust, or certain foods, use over-the-counter antihistamines or nasal corticosteroids for symptom relief such as Allerta and Cetirizine, keep windows closed and use air purifiers to reduce indoor allergens, consider allergy shots (immunotherapy) for long-term management of allergies.", "z-img/medicine/allerta.png", ["Allerta", "Cetirizine"]),
    
    (["sinus", "sinus infection"], "Use saline nasal rinses or sprays to clear nasal passages, apply warm compresses to the face to relieve sinus pressure, stay hydrated to help thin mucus and promote drainage, use over-the-counter decongestants or pain relievers for symptom relief like Sinutabs, consult a healthcare professional if symptoms persist or worsen.", "z-img/medicine/sinutab.jpg", ["Sinutab"]),
    (["edema", "fluid retention", "fat", "increased weight"], "Limit salt intake to reduce fluid retention, elevate legs when resting to promote fluid drainage, wear compression stockings if recommended by a healthcare professional, engage in regular physical activity to improve circulation, monitor weight and report sudden or significant increases to a healthcare provider.", None, [""]),
    (["hearing", "hearing problems", "hear"], "Schedule a hearing evaluation with an audiologist, avoid exposure to loud noises and use ear protection when necessary, consider hearing aids if recommended by a healthcare professional, communicate openly with family and friends about hearing difficulties, explore assistive listening devices for improved communication.", None, [""]),
    (["painful urination", "painful urine", "red urine", "blood urine"], "Drink plenty of water to dilute urine and reduce irritation, avoid irritating substances like caffeine, alcohol, and spicy foods, practice good hygiene, such as wiping from front to back, consider over-the-counter urinary analgesics for pain relief like Ciprofloxacin, seek medical attention if pain persists or is accompanied by other symptoms.", "z-img/medicine/ciprofloxacin.jpg", ["Ciprofloxacin"]),
    (["too much sweating", "sweating", "excessive sweat", "sweat"], "Use antiperspirants containing aluminum chloride, wear loose-fitting, breathable clothing, avoid spicy foods, caffeine, and alcohol, maintain a healthy weight, consider prescription antiperspirants or procedures like botox injections or iontophoresis for severe cases.", None, [""]),
    (["pale skin", "pale"], "Ensure adequate iron intake through diet or supplements, eat foods rich in iron such as red meat, poultry, beans, and leafy green vegetables, consider iron supplementation under medical supervision, avoid prolonged sun exposure to prevent further skin damage.", None, [""]),
    (["choke", "choking"], "Perform the Heimlich maneuver if someone is choking and unable to breathe, encourage coughing to dislodge the object, seek emergency medical attention if choking persists, learn first aid techniques for choking emergencies.", None, [""]),
    (["vitamin deficiency", "deficiency"], "Take a daily multivitamin supplement containing essential vitamins and minerals, eat a varied and balanced diet rich in fruits, vegetables, whole grains, and lean proteins, consider vitamin-specific supplements if deficient in certain nutrients, consult a healthcare professional for personalized recommendations.", "z-img/medicine/neurobion.jpg", ["Neurobion", "Centrum", "Centrum Advance"]),
    (["red eyes", "bloody eyes", "red eye", "eyes are bloody", "eyes are red"], "Use over-the-counter artificial tears or eye solutions to lubricate the eyes, apply cold compresses to reduce redness and inflammation, avoid rubbing or touching the eyes, limit exposure to irritants like smoke or allergens, seek medical attention if redness persists or is accompanied by pain or vision changes.", "z-img/medicine/eye-mo.jpg", [""]),
    (["dry eyes", "dry eye", "eyes feel dry"], "Use artificial tears or lubricating eye drops regularly, use a humidifier to add moisture to indoor air, avoid exposure to dry or windy conditions, take frequent breaks when using digital screens, consult an eye doctor for prescription eye drops or other treatments if dryness persists.", "z-img/medicine/eye-mo.jpg", [""]), 
    
    (["slurred speech", "slurred", "slur", "speech", "stutter", "stammer", "mumble"], "Speak slowly and clearly, practice tongue and speech exercises recommended by a speech therapist, avoid alcohol and sedating medications that may exacerbate slurred speech, seek medical attention if slurring is sudden or accompanied by other neurological symptoms.", None, [""]),
    (["back pain", "back ache", "ache back", "pain back", "back is aching", "back feels painful"], "Maintain good posture, use ergonomic furniture and support cushions, apply heat or cold packs to the affected area, perform gentle stretching exercises and low-impact activities like walking or swimming, For faster pain relief, consider taking medications such as Muskelax or Dolfenal. Consider physical therapy or chiropractic care for long-term management.", "z-img/medicine/muskelax.png", ["Muskelax", "Dolfenal"]),
    (["leg pain", "leg ache", "ache leg", "leg is aching", "leg feels painful"], "Elevate legs and apply cold compresses to reduce swelling and inflammation, perform gentle stretching exercises, wear supportive footwear, avoid prolonged standing or sitting. For faster pain relief, consider taking pain relief medications such as Dolfenal or Ibuprofen. Consult a healthcare professional for evaluation and treatment of underlying causes.", "z-img/medicine/dolfenal.jpg", ["Dolfenal", "Ibuprofen"]),
    (["shoulder pain", "shoulder ache", "ache shoulder", "pain shoulder", "shoulder is aching", "shoulder feels painful"], "Rest the affected shoulder and avoid activities that worsen pain, apply ice packs to reduce inflammation, perform gentle shoulder exercises to improve range of motion and strength, consider physical therapy or corticosteroid injections for persistent pain.", "z-img/medicine/ammeltz.png", ["Ammeltz"]),
    (["muscle pain", "muscle ache", "pain muscle", "ache muscle", "muscle is aching", "muscle feels painful"], "Rest the affected muscles and avoid overexertion, apply heat or cold therapy to reduce pain and inflammation, gently massage the area to promote relaxation, take over-the-counter pain relievers like Ibuprofen or Acetaminophen, consider physical therapy or acupuncture for chronic muscle pain.", "z-img/medicine/skelan.png", ["Skelan"]),
    (["neck pain", "neck ache", "pain neck", "ache neck", "neck is aching", "neck feels painful"], "Practice good posture and avoid activities that strain the neck, apply heat or cold packs to the affected area, perform gentle neck stretches and exercises, use a supportive pillow and mattress, consider massage therapy or chiropractic care for relief.", "z-img/medicine/muskelax.png", ["Muskelax"]),
    (["foot pain", "foot ache", "feet ache", "feet pain", "pain foot", "pain feet", "foot", "feet", "feet is aching", "foot is aching", "feet feels painful", "foot feels painful"], "Wear supportive, well-fitted shoes with cushioned insoles, rest and elevate the affected foot, apply ice packs to reduce swelling and inflammation, perform gentle foot stretches and exercises, consider orthotic inserts or custom-made shoes for chronic foot pain.", None, [""]),
    (["hand pain", "hand ache", "hands ache", "hands pain", "hand pain", "pain hand", "pain hands", "hand", "hands", "hands feels painful"], "Rest the affected hand and avoid repetitive movements, apply ice packs to reduce swelling and inflammation, perform gentle hand exercises and stretches, use supportive splints or braces, consider hand therapy or corticosteroid injections for persistent pain.", None, [""]),
    (["body pain", "body ache", "body is aching","ache body", "pain body", "body feels painful"], "Apply heat or cold packs to the affected area, rest, use over-the-counter pain relievers like Dolfenal or Ibuprofen, and consider gentle stretching exercises.", "z-img/medicine/dolfenal.jpg", ["Dolfenal", "Ibuprofen"]),
    (["chest pain", "chest ache","chest", "pain chest", "ache chest", "chest feels aching", "chest feels painful"], "Seek immediate medical attention, especially if the chest pain is severe, prolonged, or accompanied by other symptoms such as difficulty breathing or pain radiating to the arm or jaw.", None, [""]),
    
    # Headache
    (["prevent headache", "headache prevent", "prevention for headache", "headache prevention"], "To prevent headaches, ensure you stay hydrated, maintain a healthy diet, get regular exercise, manage stress, and practice good posture. ", "z-img/biogesic.jpg"),
    (["treat headache", "headache treat", "treatment for headache", "headache treatment"], "To treat a headache, you can try over-the-counter pain relievers like ibuprofen or biogesic, rest in a quiet and dark room, apply a cold compress to your forehead, and practice relaxation techniques such as deep breathing or meditation.", "z-img/biogesic.jpg"),
    
    (["burns prevent", "prevent burns", "prevention for burns", "burn prevention"], "Always use caution when handling hot objects or liquids. Keep hot objects out of reach of children. Install smoke alarms and have a fire extinguisher at home. Treat minor burns with cool running water and cover with a clean, dry cloth.", "z-img/prevent/prevent-burn.gif"),
    (["burns treat", "treat burns", "treatment for burns", "burns treatment"], "For minor burns, run cool water over the affected area for at least 20 minutes. Do not apply ice. For severe burns, seek medical help immediately.",  "z-img/prevent/treat-burns.jpg"),
    # Cuts and Wounds
    (["cut prevent", "prevent cut", "prevention for cut", "cut prevention"], "Handle sharp objects with care. Use appropriate safety gear, such as gloves and goggles, when working with sharp tools. Keep knives and other sharp objects out of reach of children. Clean cuts thoroughly with soap and water and apply an antibiotic ointment.", "z-img/prevent/prevent-cuts.png"),
    (["cut treat", "treat cut", "treatment for cut", "cut treatment"], "Apply direct pressure to the wound to stop bleeding. Clean the wound with soap and water, and apply an antibiotic ointment. For deep cuts or wounds that won't stop bleeding, seek medical help.", "z-img/prevent/treat-cuts.png"),
    # Sprains and Strains
    (["sprain prevent", "prevent sprain", "prevention for sprain", "sprain prevention"], "Warm up before exercising or engaging in physical activity. Wear appropriate footwear that provides support. Avoid uneven surfaces. Practice proper techniques when lifting heavy objects.", "z-img/prevent/prevent-sprains.png"),
    (["sprain treat", "treat sprain", "treatment for sprain", "sprain treatment"], "Rest, ice, compress, and elevate (RICE) the affected area. Take over-the-counter pain medication if needed. Use crutches or a brace if necessary. If the pain or swelling is severe, seek medical help.", "z-img/prevent/treat-sprains.png"),
    # Fractures
    (["fracture prevent", "prevent fracture", "prevention for fracture", "fracture prevention"], "Wear appropriate protective gear when engaging in sports or activities that carry a risk of falls or collisions. Practice safety measures when driving or riding vehicles. Ensure your home is free of tripping hazards.", "z-img/prevent/prevent-fracture.png"),
    (["fracture treat", "treat fracture", "treatment for fracture", "fracture treatment"], "Immobilize the affected area to prevent further injury. Apply ice to reduce swelling. Seek medical help immediately. Do not try to realign the bone yourself.", "z-img/prevent/treat-fracture.png"),
    # Concussions
    (["concussion prevent", "prevent concussion", "prevention for concussion", "concussion prevention"], "Wear helmets during activities such as biking, skating, or playing contact sports. Avoid rough play and take precautions to prevent falls. Practice safe driving habits.", None),  #none
    (["concussion treat", "treat concussion", "treatment for concussion", "concussion treatment"], "Rest and avoid activities that could worsen symptoms, such as physical or mental exertion. Seek medical help immediately if you suspect a concussion.", "z-img/prevent/treat-concussion.png"),
    # Bruises
    (["bruises prevent", "prevent bruises", "prevention for bruises", "bruise prevention"], "Take precautions to prevent falls. Use padding or cushions on sharp corners or edges. Avoid activities with a high risk of injury.", "z-img/prevent/prevent-bruse.jpg"),
    (["bruises treat", "treat bruises", "treatment for bruises", "bruises treatment"], "Apply a cold compress to reduce swelling. Elevate the affected area. If the bruise is accompanied by severe pain or swelling, seek medical help.", "z-img/prevent/treat-bruse.jpg"),
    # Nosebleeds
    (["nosebleed prevent", "prevent nosebleed", "prevention for nosebleed", "nosebleed prevention"], "Avoid picking your nose or blowing it too hard. Use a humidifier to keep the air moist. Apply a thin layer of petroleum jelly like Vaseline inside your nostrils.", "z-img/prevent/prevent-nosebleed.png"),
    (["nosebleed treat", "treat nosebleed", "treatment for nosebleed", "nosebleed treatment"], "Lean forward slightly and pinch your nostrils together. Apply ice to the bridge of your nose. Seek medical help if the bleeding persists for more than 20 minutes.", "z-img/prevent/treat-nosebleed.jpg"),
    # Dislocations
    (["dislocation prevent", "prevent dislocation", "prevention for dislocation", "dislocation prevention"], "Warm up before physical activity. Strengthen muscles around joints with appropriate exercises. Use proper techniques when lifting heavy objects.", "z-img/prevent/prevent-dislocation.png"),
    (["dislocation treat", "treat dislocation", "treatment for dislocation", "dislocation treatment"], "Do not try to realign the joint yourself. Immobilize the affected area and apply ice to reduce swelling. Seek medical help immediately.", "z-img/prevent/treat-dislocation.png"),
    # Electric Shocks
    (["electric shock prevent", "prevent electric shock", "prevention for electric shock", "electric shock prevention"], "Unplug appliances before cleaning or repairing them. Keep electrical cords away from water. Use ground fault circuit interrupters (GFCIs) in areas where water is present.", "z-img/prevent/prevent-electric.jpg"),
    (["electric shock treat", "treat electric shock", "treatment for electric shock", "electric shock treatment"], "Turn off the power source immediately. Do not touch the person until you are sure the power is off. If the person is unconscious, perform CPR if you are trained to do so. Seek medical help immediately.", "z-img/prevent/treat-electric.png"),
    # Eye Injuries
    (["eye injuries prevent", "prevent eye injuries", "prevention for eye injuries", "eye injury prevention"], "Wear appropriate eye protection when working with hazardous materials or engaging in activities with a risk of eye injury. Avoid rubbing your eyes.", "z-img/prevent/prevent-eyes.jpg"),
    (["eye injuries treat", "treat eye injuries", "treatment for eye injuries", "eye injuries treatment"], "Flush the eye with water for at least 15 minutes. Do not try to remove objects embedded in the eye. Seek medical help immediately.", "z-img/prevent/treat-eyes.png"),
    # Poisoning
    (["poisoning prevent", "prevent poisoning", "prevention for poisoning", "poison prevention"], "Keep household chemicals and medications out of reach of children. Store them in their original containers with child-resistant caps. Never mix household chemicals. Practice food safety measures such as proper handwashing and cooking foods to the appropriate temperature. Refrigerate perishable foods promptly.", "z-img/prevent/prevent-poison.png"),
    (["poisoning treat", "treat poisoning", "treatment for poisoning", "poisoning treatment"], "If ingested, call Poison Control immediately. Follow their instructions. Do not induce vomiting unless instructed to do so. Seek medical help immediately.  ", None), #none
    
    
    
    
    
    # Animal Bites
    (["animal bite prevent", "prevent animal bite", "prevention for animal bite", "animal bite prevention"], "Avoid approaching or disturbing animals, especially strays or wild animals. Do not provoke animals. Supervise children around animals.", None),   #none
    (["animal bite treat", "treat animal bite", "treatment for animal bite", "animal bite treatment"], "Wash the wound with soap and water. Apply an antibiotic ointment and cover with a clean bandage. Seek medical help, especially if the bite is deep or from a wild animal.", "z-img/prevent/treat-animal.png"),
    # Heat Stroke
    (["heat stroke prevent", "prevent heat stroke", "prevention for heat stroke", "heat stroke prevention"], "Stay hydrated, especially in hot weather. Wear lightweight, loose-fitting clothing. Avoid strenuous activities during the hottest parts of the day.", "z-img/prevent/prevent-heat-stroke.jpg"),
    (["heat stroke treat", "treat heat stroke", "treatment for heat stroke", "heat stroke treatment"], "Move to a cooler place and rest. Drink cool fluids if conscious. Apply cool compresses to the skin. Seek medical help immediately.", "z-img/prevent/treat-heat-stroke.png"),
    # Hypothermia
    (["hypothermia prevent", "prevent hypothermia", "prevention for hypothermia", "hypothermia prevention"], "Dress warmly in layers when outdoors in cold weather. Stay dry and avoid prolonged exposure to cold temperatures. Seek shelter if necessary.", "z-img/prevent/prevent-hypothermia.jpg"),
    (["hypothermia treat", "treat hypothermia", "treatment for hypothermia", "hypothermia treatment"], "Move to a warmer place and remove wet clothing. Wrap the person in blankets or warm clothing. Offer warm liquids if conscious. Seek medical help immediately.", "z-img/prevent/treat-hypothermia.png"),
    # Choking
    (["choking prevent", "prevent choking", "prevention for choking", "choking prevention"], "Cut food into small pieces for young children. Supervise children while eating. Avoid giving small, round foods to young children.", "z-img/prevent/prevent-chocking.png"),
    (["choking treat", "treat choking", "treatment for choking", "choking treatment"], "Perform the Heimlich maneuver if the person is conscious and choking. If the person is unconscious, perform CPR if trained to do so. Seek medical help immediately.", "z-img/prevent/treat-choke.png"),
    # Drowning
    (["drowning prevent", "prevent drowning", "prevention for drowning", "drowning prevention"], "Supervise children around water at all times. Install pool fences and use life jackets when boating. Learn CPR.", "z-img/prevent/prevent-drowning.png"),
    (["drowning treat", "treat drowning", "treatment for drowning", "drowning treatment"], "Remove the person from the water. Check for breathing and start CPR if necessary. Call emergency services immediately.", "z-img/prevent/treat-drowning.png"),
    # Snake Bites
    (["snake bites prevent", "prevent snake bites", "prevention for snake bites", "snake bite prevention"], "Wear appropriate footwear and clothing when in areas where snakes may be present. Avoid provoking or handling snakes.", "z-img/prevent/prevent-snake.png"),
    (["snake bites treat", "treat snake bites", "treatment for snake bites", "snake bites treatment"], "Keep the person calm and still. Remove jewelry or tight clothing from the affected area. Seek medical help immediately.", None),   #none
    # Frostbite
    (["frostbite prevent", "prevent frostbite", "prevention for frostbite", "frostbite prevention"], "Dress in layers and keep extremities covered in cold weather. Avoid prolonged exposure to cold temperatures and windy conditions. Keep skin dry.", "z-img/prevent/prevent-frost.png"),
    (["frostbite treat", "treat frostbite", "treatment for frostbite", "frostbite treatment"], "Gradually warm the affected area with warm (not hot) water. Do not rub the area. Seek medical help immediately.", "z-img/prevent/treat-frost.jpg"),
    # Asthma Attack
    (["asthma attack prevent", "prevent asthma attack", "prevention for asthma attack", "asthma attack prevention"], "Avoid triggers such as allergens, smoke, and pollution. Take prescribed medications regularly. Keep rescue inhaler on hand.", None), #none
    (["asthma attack treat", "treat asthma attack", "treatment for asthma attack", "asthma attack treatment"], "Use rescue inhaler as prescribed. Sit upright and remain calm. Seek medical help if symptoms do not improve or worsen.", "z-img/prevent/treat-asthma.png"),   
    # Allergic Reaction
    (["allergic reaction prevent", "prevent allergic reaction", "prevention for allergic reaction", "allergic reaction prevention"], "Avoid known allergens. Carry an epinephrine auto-injector if prescribed. Wear a medical alert bracelet.", None),  #none
    (["allergic reaction treat", "treat allergic reaction", "treatment for allergic reaction", "allergic reaction treatment"], "Administer epinephrine auto-injector if available. Seek emergency medical help immediately.", "z-img/prevent/treat-allergy.png"),
    # Heart Attack
    (["heart attack prevent", "prevent heart attack", "prevention for heart attack", "heart attack prevention"], "Maintain a healthy diet and weight. Exercise regularly. Manage stress. Avoid smoking and excessive alcohol consumption.", "z-img/prevent/prevent-heart.png"),
    (["heart attack treat", "treat heart attack", "treatment for heart attack", "heart attack treatment"], "Call emergency services immediately. Chew aspirin if not allergic. Keep person calm and comfortable until help arrives.", "z-img/prevent/treat-heart.png"),
    # Stroke
    (["stroke prevent", "prevent stroke", "prevention for stroke", "stroke prevention"], "Control high blood pressure, cholesterol, and diabetes. Exercise regularly. Maintain a healthy diet. Avoid smoking and excessive alcohol consumption.", "z-img/prevent/prevent-stroke.jpg"),
    (["stroke treat", "treat stroke", "treatment for stroke", "stroke treatment"], "Call emergency services immediately. Note the time when symptoms started. Keep person calm and monitor vital signs until help arrives.", "z-img/prevent/treat-stroke.png"),
    # Severe Bleeding
    (["severe bleeding prevent", "prevent severe bleeding", "prevention for severe bleeding", "severe bleeding prevention"], "Handle sharp objects with care. Wear protective gloves when necessary. Keep first aid supplies readily available.", "z-img/prevent/prevent-cuts.png"),
    (["severe bleeding treat", "treat severe bleeding", "treatment for severe bleeding", "severe bleeding treatment"], "Apply direct pressure to the wound with a clean cloth. Elevate the wound above the heart if possible. Seek medical help immediately.", "z-img/prevent/treat-cuts.png"),
    # Seizure
    (["seizure prevent", "prevent seizure", "prevention for seizure", "seizure prevention"], "Take prescribed medications regularly. Get enough sleep. Avoid triggers such as stress, alcohol, and flashing lights.", None),  #none
    (["seizure treat", "treat seizure", "treatment for seizure", "seizure treatment"], "Keep the person safe from injury. Do not restrain them. Protect their head from injury. Stay with them until the seizure ends.", None),  #none
    # Fainting
    (["fainting prevent", "prevent fainting", "prevention for fainting", "fainting prevention"], "Avoid triggers such as standing for long periods, dehydration, and heat. Sit or lie down if feeling faint.", "z-img/prevent/prevent-fainting.png"),
    (["fainting treat", "treat fainting", "treatment for fainting", "fainting treatment"], "Lay the person flat on their back and raise their legs. Loosen tight clothing. Check for breathing and pulse. Seek medical help if necessary.", "z-img/prevent/treat-fainting.png"),
    # Heat Exhaustion
    (["heat exhaustion prevent", "prevent heat exhaustion", "prevention for heat exhaustion", "heat exhaustion prevention"], "Stay hydrated. Avoid strenuous activities in hot weather. Take breaks in shaded or air-conditioned areas.", "z-img/prevent/prevent-heatex.png"),
    (["heat exhaustion treat", "treat heat exhaustion", "treatment for heat exhaustion", "heat exhaustion treatment"], "Move to a cooler place. Remove excess clothing. Drink cool fluids. Apply cool compresses. Seek medical help if symptoms worsen or last longer than 1 hour.", "z-img/prevent/treat-heatex.png"),
  
   
   












    (["carbon monoxide poisoning prevent", "prevent carbon monoxide poisoning", "prevention for carbon monoxide poisoning", "carbon monoxide poisoning prevention"], "Install carbon monoxide detectors in your home. Ensure proper ventilation of gas appliances. Never use charcoal grills or generators indoors.", None),
    (["carbon monoxide poisoning treat", "treat carbon monoxide poisoning", "treatment for carbon monoxide poisoning", "carbon monoxide poisoning treatment"], "Move to fresh air immediately. Seek medical help. Do not re-enter the area until it has been declared safe by authorities.", None),
    # Anaphylaxis
    (["anaphylaxis prevent", "prevent anaphylaxis", "prevention for anaphylaxis", "anaphylaxis prevention"], "Avoid known allergens. Carry an epinephrine auto-injector if prescribed. Wear a medical alert bracelet.", None),
    (["anaphylaxis treat", "treat anaphylaxis", "treatment for anaphylaxis", "anaphylaxis treatment"], "Administer epinephrine auto-injector if available. Seek emergency medical help immediately.", None),
    # Eye Irritation
    (["eye irritation prevent", "prevent eye irritation", "prevention for eye irritation", "eye irritation prevention"], "Avoid rubbing your eyes. Wear protective eyewear when necessary, such as when working with chemicals or participating in sports.", None),
    (["eye irritation treat", "treat eye irritation", "treatment for eye irritation", "eye irritation treatment"], "Flush the eye with clean water for several minutes. Remove contact lenses if applicable. Seek medical help if irritation persists or worsens.", None),
    # Puncture Wounds
    (["puncture wounds prevent", "prevent puncture wounds", "prevention for puncture wounds", "puncture wounds prevention"], "Wear sturdy shoes when walking outdoors. Use caution when handling sharp objects or working with tools. Keep objects out of reach of children.", None),
    (["puncture wounds treat", "treat puncture wounds", "treatment for puncture wounds", "puncture wounds treatment"], "Clean the wound with soap and water. Apply an antibiotic ointment and cover with a sterile bandage. Seek medical help if the wound is deep or becomes infected.", None),
    # Sunburn
    (["sunburn prevent", "prevent sunburn", "prevention for sunburn", "sunburn prevention"], "Apply sunscreen with a high SPF before going outdoors. Wear protective clothing, such as hats and sunglasses. Seek shade during peak sun hours.", None),
    (["sunburn treat", "treat sunburn", "treatment for sunburn", "sunburn treatment"], "Take a cool bath or apply cool compresses to the affected area. Moisturize with aloe vera or an unscented lotion. Take over-the-counter pain relievers if needed.", None),
    # Dehydration
    (["dehydration prevent", "prevent dehydration", "prevention for dehydration", "dehydration prevention"], "Drink plenty of fluids throughout the day, especially in hot weather or during physical activity. Eat foods with high water content, such as fruits and vegetables.", None),
    (["dehydration treat", "treat dehydration", "treatment for dehydration", "dehydration treatment"], "Drink water or oral rehydration solutions to replenish fluids. Rest in a cool, shaded area. Seek medical help if symptoms are severe or persistent.", None),
    # Altitude Sickness
    (["altitude sickness prevent", "prevent altitude sickness", "prevention for altitude sickness", "altitude sickness prevention"], "Gradually ascend to higher altitudes to acclimatize. Stay hydrated. Avoid alcohol and strenuous exercise for the first few days at altitude.", None),
    (["altitude sickness treat", "treat altitude sickness", "treatment for altitude sickness", "altitude sickness treatment"], "Descend to a lower altitude if symptoms are severe. Rest and drink plenty of fluids. Seek medical help if symptoms worsen or do not improve.", None),
    # Overexertion
    (["overexertion prevent", "prevent overexertion", "prevention for overexertion", "overexertion prevention"], "Gradually increase the intensity and duration of exercise. Take breaks as needed. Stay hydrated and maintain a balanced diet.", None),
    (["overexertion treat", "treat overexertion", "treatment for overexertion", "overexertion treatment"], "Rest and drink water or electrolyte-rich fluids. Apply ice packs to sore muscles. Seek medical help if symptoms are severe or persistent.", None),
    # Smoke Inhalation
    (["smoke inhalation prevent", "prevent smoke inhalation", "prevention for smoke inhalation", "smoke inhalation prevention"], "Install smoke alarms in your home and test them regularly. Have a fire escape plan and practice it with your family. Avoid smoking indoors.", None),
    (["smoke inhalation treat", "treat smoke inhalation", "treatment for smoke inhalation", "smoke inhalation treatment"], "Move to fresh air immediately. Seek medical help if experiencing difficulty breathing, coughing, or other symptoms of smoke inhalation.", None),
    # Road Rash
    (["road rash prevent", "prevent road rash", "prevention for road rash", "road rash prevention"], "Wear appropriate protective gear when cycling, skateboarding, or participating in other activities with a risk of falling. Avoid speeding and follow traffic laws.", None),
    (["road rash treat", "treat road rash", "treatment for road rash", "road rash treatment"], "Clean the wound with soap and water. Apply an antibiotic ointment and cover with a sterile bandage. Seek medical help if the wound is deep or becomes infected.", None),
    # Sore Throat
    (["sore throat prevent", "prevent sore throat", "prevention for sore throat", "sore throat prevention"], "Practice good hygiene, such as washing hands frequently and avoiding close contact with sick individuals. Avoid smoking and exposure to secondhand smoke.", None),
    (["sore throat treat", "treat sore throat", "treatment for sore throat", "sore throat treatment"], "Rest and stay hydrated. Gargle with warm salt water. Use over-the-counter pain relievers or lozenges for relief. Seek medical help if symptoms persist or worsen.", None),
    # Hangover
    (["hangover prevent", "prevent hangover", "prevention for hangover", "hangover prevention"], "Drink alcohol in moderation. Stay hydrated by drinking water between alcoholic beverages. Eat a meal before drinking.", None),
    (["hangover treat", "treat hangover", "treatment for hangover", "hangover treatment"], "Stay hydrated with water or electrolyte-rich fluids. Eat a balanced meal. Get plenty of rest. Use over-the-counter pain relievers if needed.", None),
    # Indigestion
    (["indigestion prevent", "prevent indigestion", "prevention for indigestion", "indigestion prevention"], "Eat smaller, more frequent meals. Avoid trigger foods that cause indigestion, such as spicy or fatty foods. Eat slowly and chew food thoroughly.", None),
    (["indigestion treat", "treat indigestion", "treatment for indigestion", "indigestion treatment"], "Take over-the-counter antacids or acid reducers. Drink water or herbal tea. Avoid lying down immediately after eating. Seek medical help if symptoms are severe or persistent.", None),
    # Motion Sickness
    (["motion sickness prevent", "prevent motion sickness", "prevention for motion sickness", "motion sickness prevention"], "Choose a seat where motion is felt the least, such as over the wings on an airplane or near the front in a car. Focus on the horizon or a stationary object.", None),
    (["motion sickness treat", "treat motion sickness", "treatment for motion sickness", "motion sickness treatment"], "Rest and get fresh air. Drink ginger tea or take ginger supplements. Use over-the-counter medications such as dimenhydrinate or meclizine.", None),
    # Insomnia
    (["insomnia prevent", "prevent insomnia", "prevention for insomnia", "insomnia prevention"], "Maintain a regular sleep schedule. Create a relaxing bedtime routine. Avoid caffeine and electronic devices before bedtime.", None),
    (["insomnia treat", "treat insomnia", "treatment for insomnia", "insomnia treatment"], "Create a comfortable sleep environment. Limit naps during the day. Practice relaxation techniques such as deep breathing or meditation. Seek medical help if insomnia persists.", None),
    # Jet Lag
    (["jet lag prevent", "prevent jet lag", "prevention for jet lag", "jet lag prevention"], "Gradually adjust sleep and meal times to the destination's time zone before traveling. Stay hydrated. Get exposure to natural sunlight upon arrival.", None),
    (["jet lag treat", "treat jet lag", "treatment for jet lag", "jet lag treatment"], "Stay hydrated. Get exposure to natural sunlight during the day. Take short naps if needed. Allow time for your body to adjust to the new time zone.", None),
    # Acne
    (["acne prevent", "prevent acne", "prevention for acne", "acne prevention"], "Wash your face twice daily with a gentle cleanser. Avoid touching your face. Use non-comedogenic skincare products.", None),
    (["acne treat", "treat acne", "treatment for acne", "acne treatment"], "Use over-the-counter or prescription acne treatments as directed. Avoid picking or squeezing acne lesions. Follow a consistent skincare routine.", None),
    # Headache
    (["headache prevent", "prevent headache", "prevention for headache", "headache prevention"], "Stay hydrated. Practice good posture. Manage stress with relaxation techniques such as deep breathing or meditation.", None),
    (["headache treat", "treat headache", "treatment for headache", "headache treatment"], "Rest in a quiet, dark room. Apply a cold compress to the forehead. Take over-the-counter pain relievers as needed.", None),
    # Migraine
    (["migraine prevent", "prevent migraine", "prevention for migraine", "migraine prevention"], "Identify and avoid triggers such as certain foods, stress, or lack of sleep. Maintain a regular sleep schedule. Stay hydrated.", None),
    (["migraine treat", "treat migraine", "treatment for migraine", "migraine treatment"], "Rest in a quiet, dark room. Apply a cold compress to the forehead. Take prescribed migraine medications as directed.", None),
    # Back Pain
    (["back pain prevent", "prevent back pain", "prevention for back pain", "back pain prevention"], "Practice good posture. Lift heavy objects with your legs, not your back. Exercise regularly to strengthen back muscles.", None),
    (["back pain treat", "treat back pain", "treatment for back pain", "back pain treatment"], "Apply heat or cold packs to the affected area. Take over-the-counter pain relievers as needed. Practice gentle stretching and exercise.", None),
    # Toothache
    (["toothache prevent", "prevent toothache", "prevention for toothache", "toothache prevention"], "Brush your teeth twice daily with fluoride toothpaste. Floss daily. Avoid sugary foods and drinks. Visit your dentist regularly for check-ups.", None),
    (["toothache treat", "treat toothache", "treatment for toothache", "toothache treatment"], "Rinse your mouth with warm salt water. Use over-the-counter pain relievers. Apply a cold compress to the cheek. See your dentist if pain persists.", None),
    # Diarrhea
    (["diarrhea prevent", "prevent diarrhea", "prevention for diarrhea", "diarrhea prevention"], "Wash your hands frequently, especially before eating or preparing food. Drink clean, bottled water when traveling to areas with poor sanitation.", None),
    (["diarrhea treat", "treat diarrhea", "treatment for diarrhea", "diarrhea treatment"], "Stay hydrated with clear fluids. Eat bland foods such as rice, bananas, and toast. Avoid dairy products and caffeine. Seek medical help if symptoms are severe or last longer than a few days.", None),
    # Constipation
    (["constipation prevent", "prevent constipation", "prevention for constipation", "constipation prevention"], "Eat a high-fiber diet rich in fruits, vegetables, and whole grains. Drink plenty of water. Exercise regularly.", None),
    (["constipation treat", "treat constipation", "treatment for constipation", "constipation treatment"], "Increase fiber intake with foods or supplements. Stay hydrated. Exercise regularly. Use over-the-counter laxatives if needed.", None),
    # Acid Reflux
    (["acid reflux prevent", "prevent acid reflux", "prevention for acid reflux", "acid reflux prevention"], "Avoid trigger foods such as spicy or fatty foods, caffeine, and citrus. Eat smaller, more frequent meals. Maintain a healthy weight.", None),
    (["acid reflux treat", "treat acid reflux", "treatment for acid reflux", "acid reflux treatment"], "Take over-the-counter antacids or acid reducers. Avoid lying down immediately after eating. Elevate the head of your bed. Avoid trigger foods.", None),
    # Nausea
    (["nausea prevent", "prevent nausea", "prevention for nausea", "nausea prevention"], "Eat smaller, more frequent meals. Stay hydrated with clear fluids. Avoid strong odors and trigger foods.", None),
    (["nausea treat", "treat nausea", "treatment for nausea", "nausea treatment"], "Rest in a quiet, dark room. Drink clear fluids such as water, ginger ale, or broth. Try over-the-counter medications such as bismuth subsalicylate or dimenhydrinate.", None),
    # Acidosis
    (["acidosis prevent", "prevent acidosis", "prevention for acidosis", "acidosis prevention"], "Stay hydrated. Eat a balanced diet with plenty of fruits and vegetables. Avoid excessive alcohol consumption.", None),
    (["acidosis treat", "treat acidosis", "treatment for acidosis", "acidosis treatment"], "Treat the underlying cause, such as diabetes or kidney disease. Restore the body's acid-base balance with medications or intravenous fluids. Seek medical help immediately.", None),
    # Alkalosis
    (["alkalosis prevent", "prevent alkalosis", "prevention for alkalosis", "alkalosis prevention"], "Stay hydrated. Avoid excessive vomiting or use of diuretics. Eat a balanced diet.", None),
    (["alkalosis treat", "treat alkalosis", "treatment for alkalosis", "alkalosis treatment"], "Treat the underlying cause, such as dehydration or electrolyte imbalances. Restore the body's acid-base balance with medications or intravenous fluids. Seek medical help immediately.", None),
    # Kidney Stones
    (["kidney stones prevent", "prevent kidney stones", "prevention for kidney stones", "kidney stones prevention"], "Stay hydrated by drinking plenty of water. Eat a balanced diet with adequate calcium and low oxalate levels. Limit sodium intake.", None),
    (["kidney stones treat", "treat kidney stones", "treatment for kidney stones", "kidney stones treatment"], "Drink plenty of water to help pass the stone. Use over-the-counter pain relievers. Seek medical help if symptoms are severe or if the stone does not pass.", None),
    # Cystitis
    (["cystitis prevent", "prevent cystitis", "prevention for cystitis", "cystitis prevention"], "Stay hydrated. Urinate frequently, especially after sexual activity. Wipe from front to back after using the bathroom.", None),
    (["cystitis treat", "treat cystitis", "treatment for cystitis", "cystitis treatment"], "Drink plenty of water. Use over-the-counter pain relievers. Apply a heating pad to the abdomen. Seek medical help if symptoms persist or worsen.", None),
    # Prostatitis
    (["prostatitis prevent", "prevent prostatitis", "prevention for prostatitis", "prostatitis prevention"], "Practice safe sex. Urinate after sexual activity. Stay hydrated. Avoid prolonged sitting or bicycle riding.", None),
    (["prostatitis treat", "treat prostatitis", "treatment for prostatitis", "prostatitis treatment"], "Take prescribed antibiotics. Use over-the-counter pain relievers. Apply a heating pad to the pelvic area. Seek medical help if symptoms persist or worsen.", None),
    # Urinary Tract Infection (UTI)
    (["urinary tract infection prevent", "prevent urinary tract infection", "prevention for urinary tract infection", "urinary tract infection prevention"], "Stay hydrated. Urinate frequently. Wipe from front to back after using the bathroom. Avoid irritants such as perfumed products.", None),
    (["urinary tract infection treat", "treat urinary tract infection", "treatment for urinary tract infection", "urinary tract infection treatment"], "Take prescribed antibiotics. Drink plenty of water. Apply a heating pad to the abdomen. Seek medical help if symptoms persist or worsen.", None),
    # Dehydration
    (["dehydration prevent", "prevent dehydration", "prevention for dehydration", "dehydration prevention"], "Drink plenty of fluids throughout the day, especially in hot weather or during physical activity. Eat foods with high water content, such as fruits and vegetables.", None),
    (["dehydration treat", "treat dehydration", "treatment for dehydration", "dehydration treatment"], "Drink water or oral rehydration solutions to replenish fluids. Rest in a cool, shaded area. Seek medical help if symptoms are severe or persistent.", None),
    # Laryngitis
    (["laryngitis prevent", "prevent laryngitis", "prevention for laryngitis", "laryngitis prevention"], "Avoid smoking and exposure to secondhand smoke. Stay hydrated. Avoid overusing your voice, especially in noisy environments.", None),
    (["laryngitis treat", "treat laryngitis", "treatment for laryngitis", "laryngitis treatment"], "Rest your voice. Stay hydrated with warm liquids. Use a humidifier to add moisture to the air. Avoid irritants such as smoke or strong fumes.", None),
    # Strep Throat
    (["strep throat prevent", "prevent strep throat", "prevention for strep throat", "strep throat prevention"], "Practice good hygiene, such as washing hands frequently and avoiding close contact with sick individuals. Avoid sharing utensils or personal items.", None),
    (["strep throat treat", "treat strep throat", "treatment for strep throat", "strep throat treatment"], "Take prescribed antibiotics. Get plenty of rest. Drink warm liquids such as tea or broth. Use over-the-counter pain relievers for relief.", None),
    # Tonsillitis
    (["tonsillitis prevent", "prevent tonsillitis", "prevention for tonsillitis", "tonsillitis prevention"], "Practice good hygiene, such as washing hands frequently and avoiding close contact with sick individuals. Avoid sharing utensils or personal items.", None),
    (["tonsillitis treat", "treat tonsillitis", "treatment for tonsillitis", "tonsillitis treatment"], "Rest and stay hydrated. Gargle with warm salt water. Use over-the-counter pain relievers or throat lozenges for relief. Seek medical help if symptoms persist or worsen.", None),
    # Sinusitis
    (["sinusitis prevent", "prevent sinusitis", "prevention for sinusitis", "sinusitis prevention"], "Practice good hygiene, such as washing hands frequently. Use a humidifier to add moisture to the air. Avoid exposure to allergens or irritants.", None),
    (["sinusitis treat", "treat sinusitis", "treatment for sinusitis", "sinusitis treatment"], "Get plenty of rest. Drink fluids to stay hydrated. Use over-the-counter decongestants or saline nasal sprays. Apply warm compresses to the face.", None),
    # Bronchitis
    (["bronchitis prevent", "prevent bronchitis", "prevention for bronchitis", "bronchitis prevention"], "Avoid smoking and exposure to secondhand smoke. Practice good hygiene, such as washing hands frequently. Get vaccinated against the flu and pneumonia.", None),
    (["bronchitis treat", "treat bronchitis", "treatment for bronchitis", "bronchitis treatment"], "Get plenty of rest. Drink fluids to stay hydrated. Use over-the-counter cough suppressants or expectorants. Use a humidifier to moisten the air.", None),
    # Asthma Attack
    (["asthma attack prevent", "prevent asthma attack", "prevention for asthma attack", "asthma attack prevention"], "Identify and avoid triggers such as allergens, smoke, or exercise in cold air. Take prescribed asthma medications as directed. Get vaccinated against the flu and pneumonia.", None),
    (["asthma attack treat", "treat asthma attack", "treatment for asthma attack", "asthma attack treatment"], "Use a rescue inhaler as prescribed. Sit upright and try to remain calm. Seek medical help if symptoms do not improve or if peak flow measurements decrease.", None),
    # Pneumonia
    (["pneumonia prevent", "prevent pneumonia", "prevention for pneumonia", "pneumonia prevention"], "Get vaccinated against bacterial and viral infections such as flu and pneumococcus. Practice good hygiene, such as washing hands frequently. Avoid smoking and exposure to secondhand smoke.", None),
    (["pneumonia treat", "treat pneumonia", "treatment for pneumonia", "pneumonia treatment"], "Take prescribed antibiotics or antiviral medications. Get plenty of rest. Drink fluids to stay hydrated. Use over-the-counter pain relievers or fever reducers.", None),
    # Pulmonary Embolism
    (["pulmonary embolism prevent", "prevent pulmonary embolism", "prevention for pulmonary embolism", "pulmonary embolism prevention"], "Move around during long periods of sitting, such as during travel or work. Stay hydrated. Use compression stockings if recommended.", None),
    (["pulmonary embolism treat", "treat pulmonary embolism", "treatment for pulmonary embolism", "pulmonary embolism treatment"], "Seek emergency medical help immediately. Treatment may include blood thinners, clot-dissolving medications, or surgery.", None),
    # Hypertension (High Blood Pressure)
    (["hypertension prevent", "prevent hypertension", "prevention for hypertension", "hypertension prevention"], "Maintain a healthy weight. Exercise regularly. Limit salt intake. Avoid excessive alcohol consumption.", None),
    (["hypertension treat", "treat hypertension", "treatment for hypertension", "hypertension treatment"], "Take prescribed medications as directed. Adopt a healthy lifestyle with regular exercise and a balanced diet. Monitor blood pressure regularly.", None),
    # Hypotension (Low Blood Pressure)
    (["hypotension prevent", "prevent hypotension", "prevention for hypotension", "hypotension prevention"], "Stay hydrated. Eat small, frequent meals. Avoid prolonged standing or sudden position changes.", None),
    (["hypotension treat", "treat hypotension", "treatment for hypotension", "hypotension treatment"], "Drink fluids such as water, sports drinks, or oral rehydration solutions. Use compression stockings if recommended. Avoid alcohol and caffeine.", None),
    # Hyperglycemia (High Blood Sugar)
    (["hyperglycemia prevent", "prevent hyperglycemia", "prevention for hyperglycemia", "hyperglycemia prevention"], "Monitor blood sugar levels regularly. Follow a diabetes management plan including diet, exercise, and medication. Stay hydrated.", None),
    (["hyperglycemia treat", "treat hyperglycemia", "treatment for hyperglycemia", "hyperglycemia treatment"], "Take prescribed diabetes medications or insulin as directed. Drink water to stay hydrated. Seek medical help if blood sugar levels are consistently high or if symptoms worsen.", None),
    # Hypoglycemia (Low Blood Sugar)
    (["hypoglycemia prevent", "prevent hypoglycemia", "prevention for hypoglycemia", "hypoglycemia prevention"], "Eat regular meals and snacks. Monitor blood sugar levels regularly. Carry a fast-acting source of glucose such as glucose tablets or juice.", None),
    (["hypoglycemia treat", "treat hypoglycemia", "treatment for hypoglycemia", "hypoglycemia treatment"], "Consume a fast-acting source of glucose such as glucose tablets, juice, or candy. Follow up with a snack or meal containing protein and carbohydrates. Seek medical help if symptoms do not improve.", None),
    # Hyperthermia (Heat Stroke)
    (["hyperthermia prevent", "prevent hyperthermia", "prevention for hyperthermia", "hyperthermia prevention"], "Stay hydrated. Avoid strenuous activity in hot, humid weather. Wear lightweight, light-colored clothing. Take breaks in the shade.", None),
    (["hyperthermia treat", "treat hyperthermia", "treatment for hyperthermia", "hyperthermia treatment"], "Move to a cooler environment. Drink cool fluids. Apply cool compresses or ice packs to the body. Seek emergency medical help immediately.", None),
    # Hypothermia
    (["hypothermia prevent", "prevent hypothermia", "prevention for hypothermia", "hypothermia prevention"], "Wear warm clothing in cold weather. Stay dry and change out of wet clothes promptly. Limit time spent outdoors in extreme cold.", None),
    (["hypothermia treat", "treat hypothermia", "treatment for hypothermia", "hypothermia treatment"], "Move to a warmer environment. Remove wet clothing and replace with dry clothes. Wrap in blankets or use a sleeping bag to increase body temperature. Seek medical help immediately.", None),
]

fallback_response = "I'm sorry, I'm not trained to answer that question."





def generate_response(message):
    # Initialize variables to track maximum score and corresponding response
    best_response = fallback_response
    best_image = None
    
    # Iterate over the dataset to find the best matching response
    for keywords, response, img in dataset:
        # Check for exact matches first
        if any(keyword.lower() in message.lower() for keyword in keywords):
            best_response = response
            best_image = img
            break
        
        # If no exact matches, check for partial matches
        for keyword in keywords:
            if difflib.SequenceMatcher(None, keyword.lower(), message.lower()).ratio() >= 0.7:
                best_response = response
                best_image = img
                break
    
    return best_response, best_image






class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            if self.path.endswith('.html'):
                mimetype = 'text/html'
            elif self.path.endswith('.css'):
                mimetype = 'text/css'
            elif self.path.endswith('.js'):
                mimetype = 'application/javascript'
            elif self.path.endswith('.png'):
                mimetype = 'image/png'
            elif self.path.endswith('.jpg'):
                mimetype = 'image/jpg'
            elif self.path.endswith('.gif'):
                mimetype = 'image/gif'
            else:
                raise Exception('Unknown file type')
                
            # Open and read the file
            with open(self.path[1:], 'rb') as file:
                content = file.read()
                
            # Set response code and headers
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            
            # Send the content of the file
            self.wfile.write(content)
        except Exception as e:
            print(f'Error: {e}')
            self.send_error(404, 'File Not Found')








    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if 'audio' in data:
            # Speech-to-text conversion
            audio_data = data['audio']
            text = self.convert_audio_to_text(audio_data)
            message = text.strip()
        else:
            message = data['message']

        response, image_path = generate_response(message)

        # Send the JSON response with the bot's text response and image path to the client
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Include the chathead image and image path in the JSON response
        chathead_image = 'MICA_chathead4.png'  # Path to the chathead image
        response_data = {
            'response': response,
            'chathead': chathead_image,
            'image': image_path
        }
        self.wfile.write(json.dumps(response_data).encode())







    def convert_audio_to_text(self, audio_data):
        recognizer = sr.Recognizer()
        with sr.AudioData(audio_data) as audio_file:
            try:
                text = recognizer.recognize_google(audio_file)
                return text
            except sr.UnknownValueError:
                return ""
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()
