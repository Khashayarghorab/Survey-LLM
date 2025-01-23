import streamlit as st
import pandas as pd
import random
import re
import json
import os
from io import StringIO
from google.oauth2 import service_account
import gspread

# Initialize default answers for A and B
initial_questions = [

    {"question": "Repairing and Sealing Roof Leaks.", "A": """### Job Safety Analysis (JSA) – Repairing and Sealing Roof Leaks

#### **Scope of Work**
The task involves repairing and sealing leaks on a roof. Activities include accessing the roof, identifying and preparing the leak areas, applying sealant/repair materials, and finishing with cleanup. The process requires working at heights, using specialized tools, and handling potentially hazardous materials. Ensuring the safety of workers and minimizing risks of injury or environmental harm are paramount.

#### Table: Job Steps, Hazards, Risk Assessment, and Preventive Measures

| **Job Step**                                         | **Hazard**                                                                                     | **Likelihood (P)** | **Impact (C)** | **Preventive Measures**                                                                                      |
|------------------------------------------------------|-----------------------------------------------------------------------------------------------|---------------------|----------------|--------------------------------------------------------------------------------------------------------------|
| **1. Preparing the Work Area**                       | Tripping hazards due to tools or debris                                                      | P4: Possible        | C2: Minor       | Keep tools organized and clear debris to ensure a clean workspace.                                           |
|                                                      | Exposure to weather conditions (heat, rain, UV, etc.)                                        | P5: Likely          | C2: Minor       | Provide PPE (e.g., hats, sunscreen, weather-appropriate clothing). Take rest breaks in shaded areas.          |
| **2. Accessing the Roof**                            | Falls from height (e.g., while climbing ladders or scaffolding)                              | P5: Likely          | C5: Major       | Use secured ladders/scaffolding inspected for stability. Employ harnesses and fall arrest systems.           |
|                                                      | Structural failure of the roof (e.g., stepping on weak areas)                                | P4: Possible        | C4: Significant | Inspect the roof for weak spots. Mark vulnerable areas and use platforms to distribute weight if necessary.   |
|                                                      | Slips on wet or slippery surfaces                                                           | P4: Possible        | C3: Moderate    | Wear non-slip footwear. Ensure the roof is dry before accessing.                                             |
| **3. Identifying and Preparing Leak Areas**          | Exposure to potentially toxic/dusty materials (e.g., sealing chemicals, old shingles)       | P3: Unlikely        | C3: Moderate    | Use respiratory masks and gloves. Provide ventilation. Review Material Safety Data Sheets (MSDS).            |
|                                                      | Cuts or abrasions from tools or sharp roofing materials                                      | P4: Possible        | C2: Minor       | Train workers in safe tool use. Wear gloves and use appropriate tools.                                       |
| **4. Applying Sealant and Repair Materials**         | Chemical exposure from sealants (skin/eye irritation or fumes)                               | P4: Possible        | C3: Moderate    | Provide gloves, goggles, and adequate ventilation. Follow manufacturer guidelines for handling materials.     |
|                                                      | Falling objects (e.g., tools or materials)                                                  | P4: Possible        | C4: Significant | Use tool lanyards to tether equipment. Restrict access below work areas.                                     |
|                                                      | Electrical hazards (e.g., contact with overhead wires or roof-mounted equipment)            | P3: Unlikely        | C5: Major       | Inspect work area for electrical hazards. Maintain a safe distance from electrical equipment.                |
| **5. Cleaning Up and Leaving the Work Area**         | Lifting and carrying injuries (e.g., strains, sprains)                                      | P4: Possible        | C2: Minor       | Use proper lifting techniques. Ensure loads are manageable. Use team lifting if necessary.                   |
|                                                      | Slipping or falling when descending from the roof or ladder                                  | P4: Possible        | C4: Significant | Use three-point contact on ladders. Inspect ladder's base for stability.                                     |

---

### **Summary of Risk Assessment**
- **High Risk (Likelihood P4+ and Impact C4+):**
  - Falls from height during roof access.
  - Structural failure of the roof.
  - Falling objects during application of repair materials.
  - Electrical hazards.

- **Moderate Risk (P4+ and Impact C3+):**
  - Slips on the roof.
  - Chemical exposure from sealants.
  - Injuries from slippery surfaces or sharp materials/tools.

- **Low Risk:**
  - Weather exposure during preparation.
  - Cuts and abrasions from tools.
  - Lifting and carrying sprains during cleanup.

---

### **Recommendations and Preventive Strategies**
1. **Fall Prevention:** Always utilize a fall arrest system (harnesses, lanyards, lifelines) and conduct pre-task roof inspections to identify weak spots or hazards. Train workers in fall safety protocols.
2. **Roof Stability:** Inspect all work areas before starting tasks. Add supports like work platforms where necessary.
3. **PPE and Safety Equipment:** Provide appropriate PPE, including gloves, goggles, helmets, and slip-resistant footwear. Ensure respiratory masks are available for work involving dusty or chemical environments.
4. **Safe Material Handling:** Train workers on the safe use of tools and correct lifting techniques. Tether tools to prevent falling hazards.
5. **Adherence to Safety Protocols:** Include job hazard briefing before starting the task. Regularly inspect safety equipment and tools.

---

### Finalized Job Safety Analysis Report
The job safety analysis for repairing and sealing roof leaks identifies critical hazards related to falls from height, structural failures, chemical exposure, and slipping risks. With appropriate preventive measures, such as inspection processes, worker training, use of PPE, and safe operational practices, the job can proceed efficiently and safely. Managers and supervisors must monitor compliance with safety protocols and provide a culture of proactive hazard management. A specific emergency response procedure should also be in place, especially for high-risk tasks, ensuring swift action in case of incidents.""", "B": """**Final Report: Job Safety Analysis (JSA) for Repairing and Sealing Roof Leaks**\n\n---\n\n### **Scope of Work:**  \nThe task involves identifying, repairing, and sealing roof leaks to prevent water intrusion and further damage. This includes inspecting the roof, locating leaks, repairing damaged areas, and applying appropriate sealing materials.\n\n---\n\n### **Job Steps, Hazards, Risk Assessments, and Preventive Measures**\n\n| **Job Step**                     | **Hazard**                                                                 | **Likelihood (P)** | **Impact (C)** | **Preventive Measures**                                                                                     |\n|-----------------------------------|-----------------------------------------------------------------------------|---------------------|----------------|-------------------------------------------------------------------------------------------------------------|\n| **Preparation and Safety Setup** | Falls from height due to improper ladder or scaffolding setup               | P5 (Likely)         | C5 (Major)     | Conduct daily inspections, provide training, and use fall arrest systems.                                   |\n|                                   | Slips, trips, and falls caused by debris or obstacles                       | P4 (Possible)       | C3 (Moderate)  | Enforce housekeeping protocols, assign a safety officer, and conduct periodic safety audits.                |\n|                                   | Inadequate or malfunctioning PPE                                           | P4 (Possible)       | C4 (Significant) | Inspect PPE regularly, train workers on proper use, and replace damaged PPE immediately.                    |\n| **Inspection and Leak Identification** | Falling through weak or damaged roof sections                              | P4 (Possible)       | C5 (Major)     | Use safety boards, conduct visual inspections, utilize drones, and ensure workers wear harnesses.           |\n|                                   | Exposure to adverse weather conditions                                      | P3 (Unlikely)       | C4 (Significant) | Monitor weather forecasts, provide weather-appropriate PPE, and develop contingency plans.                  |\n| **Surface Cleaning**             | Slipping on loose debris or wet surfaces                                    | P4 (Possible)       | C3 (Moderate)  | Enforce housekeeping protocols and ensure workers wear non-slip footwear.                                   |\n|                                   | Inhalation of dust or debris particles                                      | P3 (Unlikely)       | C2 (Minor)     | Provide masks or respirators and ensure proper ventilation.                                                 |\n| **Repairing Damaged Areas**      | Injuries from handling sharp tools or equipment                             | P4 (Possible)       | C3 (Moderate)  | Train workers on safe tool handling and use ergonomic tools.                                                |\n|                                   | Exposure to hazardous chemicals in roofing materials                        | P3 (Unlikely)       | C4 (Significant) | Use low-VOC materials, provide gloves and respirators, and train workers on chemical safety.                |\n| **Sealing the Roof**             | Inhaling fumes from sealants or adhesives                                   | P3 (Unlikely)       | C3 (Moderate)  | Use low-VOC materials, ensure proper ventilation, and mandate respirator use.                               |\n|                                   | Improper application leading to future structural issues                    | P4 (Possible)       | C3 (Moderate)  | Provide training, assign supervisors, and conduct periodic quality checks.                                  |\n| **Final Inspection**             | Falls during final inspection                                               | P3 (Unlikely)       | C4 (Significant) | Use harnesses, assign a spotter, and follow a safety checklist.                                             |\n|                                   | Water damage or electrical hazards during simulated rainfall testing        | P2 (Rare)           | C4 (Significant) | De-energize electrical systems, use waterproof covers, and inspect the area for hazards.                    |\n| **Cleanup and Demobilization**   | Improper disposal of hazardous waste materials                              | P3 (Unlikely)       | C3 (Moderate)  | Train workers on disposal procedures, partner with licensed companies, and document waste disposal.          |\n| **Documentation and Handover**   | Overlooking critical details in documentation                               | P3 (Unlikely)       | C2 (Minor)     | Use standardized checklists, assign a second reviewer, and implement digital tools.                         |\n|                                   | Miscommunication with the client                                            | P3 (Unlikely)       | C2 (Minor)     | Provide regular updates, use clear language, and confirm client understanding.                              |\n\n---\n\n### **Summary of Findings and Recommendations**\n\nThe Job Safety Analysis (JSA) for repairing and sealing roof leaks identified several high and moderate-risk hazards associated with the task. The most critical risks include falls from height, falling through weak roof sections, and exposure to hazardous chemicals or adverse weather conditions. These risks have been assessed with appropriate likelihood and impact ratings, and comprehensive preventive measures have been developed to mitigate them.\n\n**Key Recommendations:**\n1. **Training and Supervision:**  \n   - Ensure all workers are trained on safety protocols, proper use of equipment, and hazard recognition.  \n   - Assign supervisors to oversee high-risk activities, such as roof inspections and sealant application.\n\n2. **Safety Equipment and Inspections:**  \n   - Conduct daily inspections of ladders, scaffolding, and PPE to ensure they are in good condition.  \n   - Use fall arrest systems and safety boards to prevent falls and distribute weight on weak roof sections.\n\n3. **Environmental and Chemical Safety:**  \n   - Monitor weather conditions and suspend work during adverse weather.  \n   - Use low-VOC materials and provide adequate ventilation to minimize exposure to harmful fumes.\n\n4. **Housekeeping and Waste Management:**  \n   - Enforce strict housekeeping protocols to prevent slips, trips, and falls.  \n   - Partner with licensed waste disposal companies and document all hazardous waste disposal activities.\n\n5. **Communication and Documentation:**  \n   - Provide regular updates to the client and confirm their understanding of key points.  \n   - Use standardized checklists and digital tools to ensure thorough and accurate documentation.\n\n---\n\n### **Conclusion**\n\nThe preventive measures outlined in this report are designed to minimize risks and ensure the safety of all personnel involved in the project. By implementing these measures and adhering to the recommendations, the project can be completed efficiently and safely, with minimal risk to workers and the environment.\n\nThis report is now complete and ready for distribution to all relevant stakeholders.\n\n---\n\n****"""},
    {"question": "Exterior Painting at Heights.", "A": """### Job Safety Analysis (JSA) for Exterior Painting at Heights

#### **Project Scope:**
The task involves painting the exterior of a building at heights using scaffolding, ladders, or mobile elevated work platforms (MEWPs). Workers will use paint sprayers, rollers, and brushes. Specific activities include surface preparation, paint application, and clean-up. The task requires assessment for all risks associated with working at heights and other related hazards.

---

### **JSA Table:**

| **Job Step**               | **Hazard**                                                       | **Likelihood (P)** | **Impact (C)** | **Preventive/Control Measures**                                                                                                                                 |
|----------------------------|------------------------------------------------------------------|--------------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1. Site Setup and Access** | Uneven terrain causing trip or fall hazards.                    | P4 (Possible)      | C2 (Minor)     | Level the ground near scaffolding/ladders, conduct a site inspection, and establish clear walkways. Ensure proper personal protective equipment (PPE).          |
|                            | Improper scaffolding setup leading to collapse.                 | P3 (Unlikely)      | C5 (Major)     | Only trained and certified personnel should assemble scaffolds. Ensure scaffolding complies with local standards and conduct pre-use inspections.              |
|                            | Improper ladder positioning leading to falls.                   | P3 (Unlikely)      | C4 (Significant)| Ensure ladders are positioned on stable ground, follow a 4:1 ratio for ladder angle, and secure the top points of extension ladders.                             |
|                            | Falling tools or equipment from heights.                        | P4 (Possible)      | C4 (Significant)| Use tool lanyards, install toe boards on scaffolding, and establish exclusion zones beneath elevated work.                                                      |
| **2. Surface Preparation**  | Inhalation of hazardous dust particles from sanding.            | P4 (Possible)      | C3 (Moderate)  | Wear respirators with appropriate filters, and establish ventilation (if enclosed spaces are involved).                                                         |
|                            | Handling of chemical cleaners or solvents.                      | P4 (Possible)      | C3 (Moderate)  | Use gloves, goggles, and aprons when handling chemicals. Provide Material Safety Data Sheets (MSDS) and train workers accordingly.                              |
|                            | Contact with sharp objects or edges (glass/window frames).      | P4 (Possible)      | C2 (Minor)     | Wear cut-resistant gloves and conduct a walkthrough to identify hazardous edges before starting work.                                                           |
| **3. Paint Application**    | Height-related falls from scaffolds/ladders or MEWPs.           | P4 (Possible)      | C5 (Major)     | Use fall arrest systems (harnesses, lanyards), follow work-at-heights training, and conduct rescuer drills. Inspect all fall protection before each use.        |
|                            | Spray paint drift (potential inhalation or environmental hazard).| P4 (Possible)      | C2 (Minor)     | Wear masks rated for paint fumes, cover sensitive areas or landscaping, and ensure proper ventilation and wind monitoring.                                       |
|                            | Electrical hazards from contact with overhead lines.            | P3 (Unlikely)      | C5 (Major)     | Maintain a safe distance of at least 10 feet from power lines. Assess risks before ladder or MEWP placement.                                                    |
| **4. Clean-Up**             | Slips or falls from spilled paint or wet ground.                | P4 (Possible)      | C2 (Minor)     | Clean up spillage immediately. Use signs to mark wet areas. Wear slip-resistant footwear.                                                                       |
|                            | Incorrect chemical disposal creating environmental hazards.      | P3 (Unlikely)      | C4 (Significant)| Follow approved waste disposal procedures. Provide spill kits and train workers on safe disposal methods.                                                        |

---

### **Comprehensive Report:**

#### **1. Introduction:**
The Job Safety Analysis (JSA) examines all potential hazards associated with exterior painting at heights, including those specific to the use of scaffolds, ladders, MEWPs, and handling hazardous materials. This JSA aims to mitigate risks through hazard identification, assessment, and implementation of preventive measures to ensure a safe work environment.

#### **2. Hazard Analysis Summary:**
Various hazards were identified, including risks from working at heights, tool/equipment accidents, inhalation of hazardous substances, slips/trips, and environmental issues. The most significant risks include height-related falls (P4, C5) and scaffold collapses (P3, C5). Additional moderate risks involve handling chemicals (P4, C3) and hazardous paint spray inhalation (P4, C2).

#### **3. Key Preventive Measures:**
1. **Work at Heights:**
   - Conduct mandatory fall protection training for all workers.
   - Use certified personal fall arrest systems (harnesses and lanyards).
   - Inspect scaffolding/ladders before and after use.
   - Set up exclusion zones to prevent injuries from falling objects.

2. **Environmental Hazards:**
   - Train workers on safe handling of volatile organic compounds (VOCs).
   - Use proper respiratory PPE for sanding and paint fumes.
   - Monitor weather conditions (wind) before paint application to reduce overspray.

3. **Site Hazards:**
   - Regularly inspect and level ground before scaffolding setup.
   - Provide clear walkways with non-slip mats where necessary.

4. **Emergency Preparedness:**
   - Ensure first aid kits, emergency wash stations, and spill kits are accessible.
   - Establish fall rescue action plans and brief workers beforehand.

#### **4. Risk Summary:**
Prioritization shows height-related falls and scaffold collapses pose the highest risk due to the significant potential for fatal or life-altering injuries. Moderate risks, including chemical handling and inhalation of particulates, require regular training and appropriate PPE.

#### **5. Recommendations:**
- Place strict emphasis on training for working at heights.
- Perform daily safety inspections of all tools, equipment, and site setup.
- Ensure all workers use PPE correctly and consistently.
- Document daily activities and encourage reporting of near-miss incidents.

---

### **Conclusion:**
Exterior painting at heights is inherently high-risk but manageable with appropriate safety protocols and worker training. Implementing the recommended preventive measures and fostering a safety-first culture will help minimize hazards and ensure project success with minimal incidents. Continuous monitoring and evaluation should be conducted throughout the work to uphold safety standards effectively.""", "B": """**Job Safety Analysis (JSA) Report for Exterior Painting at Heights**  \n\nThe following table summarizes the job steps, associated high and moderate-risk hazards, their likelihood and impact assessments, and the recommended preventive measures to ensure safety during the exterior painting project:  \n\n| **Job Step**                  | **Hazard**                                                                 | **Likelihood (P)** | **Impact (C)** | **Preventive Measure**                                                                                     |\n|-------------------------------|---------------------------------------------------------------------------|--------------------|----------------|-----------------------------------------------------------------------------------------------------------|\n| Site Assessment and Preparation | Tripping or slipping on obstacles or uneven ground                        | P4                 | C2             | Conduct pre-work site inspection, remove obstacles, and ensure workers wear slip-resistant footwear.      |\n|                               | Exposure to hazardous materials (e.g., lead-based paint or mold)           | P4                 | C3             | Test for hazardous materials, provide PPE, and engage certified professionals for removal if required.    |\n| Equipment Setup               | Falls due to improper assembly or instability of scaffolding, ladders, or aerial lifts | P5                 | C5             | Train workers, inspect equipment daily, and use fall protection systems.                                  |\n|                               | Falling objects during setup                                              | P4                 | C3             | Secure tools and materials, use tool lanyards, and establish exclusion zones.                             |\n|                               | Equipment failure                                                         | P3                 | C4             | Implement routine maintenance and inspections, and replace defective equipment.                           |\n| Surface Preparation           | Slips or falls while cleaning surfaces                                    | P4                 | C3             | Provide non-slip footwear, use safety harnesses, and avoid pressure washers near power lines.             |\n|                               | Exposure to dust, debris, or harmful chemicals                            | P5                 | C3             | Provide dust masks, use dust extraction systems, and ensure proper ventilation.                           |\n|                               | Electrical hazards from contact with power lines                          | P3                 | C5             | Identify power lines, maintain safe distances, and use insulated tools.                                   |\n| Priming                       | Inhalation of fumes or exposure to skin irritants                         | P4                 | C2             | Use low-VOC primers, ensure proper ventilation, and provide gloves and respirators.                       |\n|                               | Spills or drips creating slippery surfaces                                | P4                 | C2             | Use drop cloths, clean spills immediately, and use non-slip mats.                                         |\n| Painting                      | Falls while reaching or leaning to paint difficult areas                  | P4                 | C4             | Use extendable tools, position scaffolding properly, and train workers on safe body positioning.          |\n| Quality Check                 | Falls or overreaching while inspecting painted surfaces                   | P4                 | C4             | Use aerial lifts or scaffolding, ensure fall protection, and limit inspection durations.                  |\n|                               | Missed hazards if inspections are rushed                                  | P3                 | C3             | Develop detailed checklists, allocate sufficient time, and assign experienced personnel.                  |\n| Cleanup and Equipment Removal | Injuries while dismantling scaffolding or height-access equipment         | P4                 | C3             | Train workers on safe dismantling procedures, use a team approach, and inspect equipment before removal.  |\n|                               | Improper disposal of hazardous materials                                  | P3                 | C2             | Train workers on disposal methods, provide designated containers, and engage licensed disposal services.   |\n|                               | Tripping hazards from leftover tools or materials                         | P4                 | C2             | Implement inventory systems, store tools properly, and conduct a final site walkthrough.                  |\n| Handover                      | Exposure to residual fumes or improperly cleaned areas                    | P4                 | C3             | Ensure proper ventilation, use air purifiers, and conduct a final cleanup.                                |\n| Weather-Related Risks         | High winds, rain, or adverse weather conditions                           | P4                 | C4             | Monitor weather forecasts, suspend work during adverse conditions, and use weather-resistant equipment.   |\n| Worker Fatigue                | Fatigue or overexertion for workers operating at heights                  | P3                 | C3             | Implement work-rest schedules, rotate tasks, and provide hydration and shaded rest areas.                 |\n\n---\n\n**Summary of Findings and Recommendations:**  \n\nThe exterior painting project involves several high and moderate-risk hazards, particularly related to working at heights, exposure to hazardous materials, and environmental factors. The following key recommendations are made to ensure safety:  \n\n1. **Height-Related Safety:**  \n   - Use fall protection systems, inspect scaffolding and ladders daily, and train workers on safe practices.  \n   - Position equipment properly to avoid overreaching and ensure stable access to all areas.  \n\n2. **Hazardous Material Management:**  \n   - Test for hazardous materials, provide appropriate PPE, and engage certified professionals for removal if necessary.  \n\n3. **Environmental and Weather Considerations:**  \n   - Monitor weather conditions and suspend work during adverse weather.  \n   - Use weather-resistant equipment and plan tasks to avoid high-risk periods.  \n\n4. **Worker Health and Fatigue:**  \n   - Implement work-rest schedules, rotate tasks, and provide access to hydration and shaded rest areas.  \n\n5. **Site Organization and Cleanup:**  \n   - Remove obstacles, secure tools and materials, and conduct thorough site walkthroughs to eliminate tripping hazards.  \n\n6. **Ventilation and Fume Management:**  \n   - Use low-VOC materials, ensure proper ventilation, and clean up residual materials to minimize exposure risks.  \n\nBy implementing these preventive measures, the project team can significantly reduce the likelihood and impact of identified hazards, ensuring a safe and efficient work environment.  \n\n---\n\nThis concludes the Job Safety Analysis (JSA) for the exterior painting project. The findings and recommendations should be communicated to all team members and stakeholders to ensure compliance and awareness.  \n\n****"""},
    {"question": "Concrete Pouring at Night on Highways", "A": """### Job Safety Analysis (JSA) for "Concrete Pouring at Night on Highways"

---

#### **Project Scope**
The task involves nighttime concrete pouring on highways, which is necessary due to reduced traffic and improved logistics. The objective is to complete all necessary phases, including site setup, material preparation, concrete pouring, and clean-up, while ensuring safety for workers, equipment, and nearby traffic. Due to the nature of nighttime work, additional hazards such as low visibility, fatigue, and traffic-related risks are amplified and require meticulous planning.

---

### **Breakdown of Job Steps with Hazards, Risk Assessment, and Preventive Measures**

| **Job Step**                | **Potential Hazards**                                                                                                                           | **Likelihood (P)** | **Impact (C)** | **Preventive Measures**                                                                                                        |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|----------------|------------------------------------------------------------------------------------------------------------------------------|
| 1. Site Setup               | - Poor visibility for workers during setup, leading to slips, trips, and falls.                                                                | P4 (Possible)     | C3 (Moderate)  | - Install adequate lighting at the worksite. <br> - Conduct pre-shift inspection of the site. <br> - Use reflective PPE.     |
|                             | - Worker collision with traffic during setup.                                                                                                  | P3 (Unlikely)     | C5 (Major)     | - Deploy barriers, traffic cones, and signage. <br> - Ensure a designated traffic controller is on-site.                      |
|                             | - Equipment collision during positioning (e.g., concrete truck).                                                                               | P4 (Possible)     | C4 (Significant) | - Assign an on-site flagger to guide vehicle placement. <br> - Conduct equipment inspection and pre-task safety briefing.    |
| 2. Material Preparation     | - Fatigue leading to improper handling of tools and materials.                                                                                 | P4 (Possible)     | C3 (Moderate)  | - Rotate worker tasks and implement rest breaks. <br> - Monitor workers for fatigue.                                         |
|                             | - Exposure to hazardous substances (e.g., cement dust and silica).                                                                              | P3 (Unlikely)     | C4 (Significant) | - Use masks, gloves, and protective equipment. <br> - Ensure proper material storage to reduce spills.                       |
| 3. Concrete Pouring         | - Slip, trip, or fall on wet or uneven surfaces during pouring.                                                                                 | P4 (Possible)     | C4 (Significant) | - Create designated walkways. <br> - Monitor and clean spills promptly.                                                      |
|                             | - Low visibility causing accidents or misstep during the concrete placement process.                                                            | P5 (Likely)       | C3 (Moderate)  | - Integrate portable, high-intensity floodlights. <br> - Enforce communication via radios for proper coordination.            |
|                             | - Traffic hazards from vehicles navigating near the pouring area.                                                                               | P3 (Unlikely)     | C5 (Major)     | - Create a buffer zone using barriers or traffic management teams. <br> - Inform public of ongoing operations with signage.   |
|                             | - Vibrations or noise from equipment causing hearing issues or worker fatigue.                                                                 | P4 (Possible)     | C3 (Moderate)  | - Utilize noise-dampening equipment. <br> - Ensure workers use hearing protection such as earplugs or earmuffs.              |
| 4. Post-Pour Cleanup        | - Slip, trip, or fall during removal of tools or equipment.                                                                                    | P4 (Possible)     | C3 (Moderate)  | - Clean and store tools systematically. <br> - Designate a cleanup supervisor to oversee work and ensure ground conditions.   |
|                             | - Improper handling of concrete residues causing ergonomic or musculoskeletal injuries.                                                        | P4 (Possible)     | C3 (Moderate)  | - Provide proper training for material handling. <br> - Supply tools like wheelbarrows, shovels, or hand carts for efficiency.|

---

### **Summary**

From the risk assessment carried out above, the nighttime concrete pouring activity on highways presents potential high and moderate hazards due to a combination of site-specific factors (low visibility and proximity to traffic) and task-specific risks (fatigue, tool handling, and equipment issues). Below is a breakdown of the risk levels and the comprehensive set of preventive measures required:

#### **Key Risks**
1. Traffic-related injuries (Major Impact, Unlikely Likelihood)
2. Fatigue-related mistakes (Moderate Impact, Possible Likelihood)
3. Slip, trip, and fall incidents (Significant Impact, Possible Likelihood)

#### **Recommendations**
- **Traffic Management:** Use barriers, cones, illuminated signage, and a traffic management team to isolate the work area from live traffic. Deploy flaggers and alert public road users in advance of highway work at night.
- **Lighting and Visibility:** Invest in mobile floodlighting to eliminate hazards due to low light conditions. Ensure all workers wear high-visibility PPE.
- **PPE and Equipment Use:** Provide ear protection, gloves, and masks to mitigate hearing and respiratory hazards. Inspect equipment regularly before and after shifts to ensure functionality and safety.
- **Fatigue Mitigation:** Schedule breaks and task rotation to prevent worker exhaustion. Monitor worker performance and provide additional manpower if necessary.
- **Workplace Safety Training:** Conduct safety briefings before every shift to ensure workers are aware of hazards and procedures. Assign specific supervisors to monitor adherence to protocols.

---

### **Final Recommendation**
Adherence to these risk mitigation strategies and safety protocols will reduce the likelihood and severity of identified hazards during nighttime concrete pouring. Regular monitoring, hazard reassessment, and open communication channels among the workforce will ensure a successful and safe implementation.""", "B": """### Job Safety Analysis (JSA) Table for Concrete Pouring at Night on Highways\n\n| **Job Step**          | **Hazard**                                                                 | **Likelihood** | **Impact**       | **Preventive Measure**                                                                                     |\n|------------------------|---------------------------------------------------------------------------|----------------|------------------|-----------------------------------------------------------------------------------------------------------|\n| **Site Preparation**   | Risk of vehicle collisions with workers or equipment due to insufficient or improperly placed barricades and signage. | P4: Possible   | C4: Significant | Deploy reflective barricades, cones, and signage; use flaggers and traffic controllers; coordinate with local authorities. |\n|                        | Inadequate temporary lighting leading to poor visibility.                 | P4: Possible   | C3: Moderate     | Install high-intensity temporary lighting; use backup lighting systems; conduct regular inspections.      |\n|                        | Slips, trips, and falls caused by debris or uneven surfaces.              | P4: Possible   | C3: Moderate     | Perform thorough pre-pour inspections; use checklists to ensure site cleanliness and level surfaces.      |\n| **Material Handling**  | Traffic congestion or accidents caused by poorly coordinated delivery schedules or staging area placement. | P4: Possible   | C3: Moderate     | Develop a detailed delivery schedule; use well-lit staging areas; coordinate with local authorities.      |\n|                        | Risk of injury from handling heavy materials in low-light conditions.     | P4: Possible   | C3: Moderate     | Provide lifting aids; train workers on material handling techniques; ensure proper lighting.              |\n|                        | Potential for compromised concrete quality if the mix is not checked thoroughly. | P3: Unlikely  | C4: Significant | Assign trained personnel for quality checks; use quality control protocols.                               |\n| **Equipment Setup**    | Equipment malfunction or failure due to inadequate pre-use testing or maintenance. | P4: Possible   | C4: Significant | Perform routine maintenance; conduct pre-use testing; maintain detailed inspection logs.                  |\n|                        | Risk of workers being struck by moving machinery in poorly lit areas.     | P4: Possible   | C4: Significant | Equip workers with high-visibility clothing; establish designated zones for equipment operation.          |\n|                        | Insufficient or improperly used PPE increasing the risk of injury.        | P3: Unlikely   | C3: Moderate     | Conduct regular PPE inspections; train workers on proper PPE use.                                         |\n| **Concrete Pouring**   | Worker fatigue or reduced alertness due to night shifts.                  | P5: Likely     | C3: Moderate     | Implement shift rotations; provide adequate breaks; monitor worker alertness.                             |\n|                        | Airborne dust or fumes from concrete mixing causing respiratory issues.   | P4: Possible   | C3: Moderate     | Use dust suppression measures; ensure proper ventilation; provide respirators.                            |\n| **Finishing**          | Risk of workers slipping on wet concrete during smoothing and leveling.   | P4: Possible   | C2: Minor        | Use anti-slip mats or footwear; train workers on proper tool use.                                         |\n|                        | Premature drying of concrete due to improper application of curing compounds or blankets. | P4: Possible   | C4: Significant | Apply curing compounds evenly; monitor the curing process.                                                |\n| **Post-Pour Activities** | Improper disposal of waste materials leading to environmental hazards or fines. | P4: Possible   | C3: Moderate     | Train workers on proper waste disposal; conduct regular site inspections.                                 |\n|                        | Risk of accidents during removal of temporary lighting and barricades.    | P4: Possible   | C3: Moderate     | Remove equipment during daylight hours; use spotters in low-visibility conditions.                        |\n\n---\n\n### Final Report: Summary of Findings and Recommendations\n\n#### **Introduction**\nThe Job Safety Analysis (JSA) for concrete pouring at night on highways identified several hazards associated with site preparation, material handling, equipment setup, concrete pouring, finishing, and post-pour activities. These hazards were assessed for their likelihood and impact, and preventive measures were developed to mitigate high and moderate risks.\n\n#### **Key Findings**\n1. **High-Risk Hazards**:\n   - Vehicle collisions with workers or equipment due to insufficient barricades and signage.\n   - Equipment malfunction or failure due to inadequate pre-use testing or maintenance.\n   - Worker fatigue during night shifts, increasing the likelihood of errors or accidents.\n\n2. **Moderate-Risk Hazards**:\n   - Inadequate temporary lighting leading to poor visibility.\n   - Traffic congestion or accidents caused by poorly coordinated delivery schedules.\n   - Airborne dust or fumes from concrete mixing causing respiratory issues.\n   - Improper disposal of waste materials leading to environmental hazards or fines.\n\n3. **Low-Risk Hazards**:\n   - Slips, trips, and falls caused by debris or uneven surfaces.\n   - Risk of workers slipping on wet concrete during finishing.\n\n#### **Recommendations**\n1. **Site Preparation**:\n   - Implement comprehensive traffic management plans, including reflective signage, flaggers, and coordination with local authorities.\n   - Ensure adequate temporary lighting with backup systems and regular inspections.\n   - Conduct thorough pre-pour inspections to remove debris and level surfaces.\n\n2. **Material Handling**:\n   - Develop and adhere to detailed delivery schedules to avoid congestion.\n   - Train workers on proper material handling techniques and provide lifting aids.\n   - Assign trained personnel to inspect concrete quality upon delivery.\n\n3. **Equipment Setup**:\n   - Perform routine maintenance and pre-use testing of all equipment.\n   - Equip workers with high-visibility clothing and restrict access to equipment zones.\n   - Ensure proper use of PPE through regular inspections and training.\n\n4. **Concrete Pouring**:\n   - Rotate shifts and provide adequate breaks to manage worker fatigue.\n   - Use dust suppression measures and ensure proper ventilation to protect against airborne hazards.\n\n5. **Finishing**:\n   - Use anti-slip mats and train workers on the proper use of finishing tools.\n   - Monitor the curing process to ensure compliance with design specifications.\n\n6. **Post-Pour Activities**:\n   - Remove temporary lighting and barricades during daylight hours whenever possible.\n   - Train workers on proper waste disposal and conduct regular site inspections.\n\n#### **Conclusion**\nThe preventive measures outlined in this report are designed to address the identified hazards and reduce the likelihood and impact of risks associated with nighttime concrete pouring on highways. By implementing these measures, the project team can enhance safety, minimize delays, and ensure compliance with industry standards and regulations.\n\n---\n\n ****"""},
    {"question": "Scaffolding Assembly and Disassembly", "A": """### Job Safety Analysis (JSA) for Scaffolding Assembly and Disassembly

---

#### **Project Scope:**
This JSA evaluates the steps, potential hazards, and mitigation measures involved in the safe assembly and disassembly of scaffolding structures at a construction site. The JSA aims to ensure efficient, hazard-free operations by assessing risks and implementing preventive controls.

---

### **Job Steps, Hazards, Risk Assessment, and Preventive Measures:**

| **Job Step**                             | **Hazard**                                                                                         | **Likelihood (P)** | **Impact (C)** | **Preventive Measures**                                                                                             |
|------------------------------------------|----------------------------------------------------------------------------------------------------|--------------------|----------------|--------------------------------------------------------------------------------------------------------------------|
| **1. Transporting scaffolding materials** | Manual handling injuries (e.g., sprains, strains, back injuries)                                    | P5 (Likely)        | C2 (Minor)     | **Preventive Measures**: Provide proper manual handling training. Use mechanical aids or team lifting for heavy materials. |
|                                          | Trips and slips while carrying materials                                                          | P4 (Possible)      | C3 (Moderate)  | Keep walkways clear of debris. Ensure proper footwear with slip-resistant soles is worn. Clean up spills immediately. |
| **2. Setting up the base (foundation)**   | Uneven or unstable ground leading to scaffold collapse                                             | P4 (Possible)      | C4 (Significant) | Level the ground before starting. Use base plates or mud sills for stability. Conduct inspections before work begins.  |
|                                          | Pinching fingers when assembling base plates                                                      | P4 (Possible)      | C2 (Minor)     | Wear gloves made of high dexterity material. Practice safe handling techniques.                                      |
| **3. Assembling scaffolding structure**   | Falls from height during assembly                                                                 | P5 (Likely)        | C5 (Major)     | Workers should use fall protection (e.g., harnesses and lanyards). Secure guardrails and maintain three points of contact when climbing. |
|                                          | Dropped objects striking other workers below                                                     | P4 (Possible)      | C4 (Significant) | Use toe boards and tool lanyards. Establish a no-go zone directly beneath the scaffolding during assembly.           |
|                                          | Collapsing or tipping scaffold due to incorrect assembly                                          | P3 (Unlikely)      | C5 (Major)     | Follow manufacturer assembly instructions. Management to inspect the scaffold at regular intervals during assembly.  |
| **4. Securing the scaffold**              | Scaffold tipping or collapsing due to improper anchoring                                          | P3 (Unlikely)      | C4 (Significant) | Use adequate tie-backs or anchors according to regulations. Perform inspection before final usage sign-off.           |
| **5. Using scaffolding during assembly**  | Overloading scaffold components during assembly                                                   | P4 (Possible)      | C4 (Significant) | Adhere to manufacturer load limits. Avoid storing excessive materials on incomplete scaffolds.                        |
|                                          | Electrical shock from overhead power lines                                                       | P3 (Unlikely)      | C6 (Catastrophic) | Perform electrical hazard surveys before starting. Maintain a safe working distance from power lines or de-energize lines. |
| **6. Disassembly of scaffolding**         | Falls from height during disassembly                                                              | P4 (Possible)      | C5 (Major)     | Wear full-body harnesses. Remove scaffolding components from the bottom first. Avoid leaning out or overreaching.     |
|                                          | Injuries from falling objects (e.g., scaffolding parts dropped during disassembly)                | P4 (Possible)      | C3 (Moderate)  | Establish an exclusion zone beneath the scaffold. Use tool lanyards and follow proper deconstruction techniques.      |
| **General hazards (all steps)**           | Weather hazards (e.g., strong winds, rain, thunderstorms)                                         | P3 (Unlikely)      | C4 (Significant) | Monitor weather forecasts. Cease scaffolding activities during dangerous weather conditions.                          |
|                                          | Lack of worker training or understanding of safety protocols                                      | P4 (Possible)      | C4 (Significant) | Conduct formal training for all workers on scaffolding safety. Perform competency checks before allowing work.        |

---

### **Summary of Findings and Recommendations:**

1. **Major Hazards Identified**:
   - Falls from height during assembly and disassembly present the highest risk category, with significant to catastrophic consequences. Mitigating these risks is critical.
   - Scaffold tipping or collapsing has the potential for serious injuries if not addressed with proper stabilization and anchoring.
   - Manual handling injuries and hazards related to dropped objects or electrical hazards also require strict control measures.

2. **Preventive Control Measures**:
   - Mandatory use of fall protection (harnesses, guardrails) for work at height.
   - Educating the workforce on proper scaffolding assembly and disassembly techniques through formal training programs.
   - Implementing site-specific protocols, such as designated no-go zones and regular inspections of scaffolding stability.

3. **Inspection and Maintenance**:
   - Before, during, and after assembly, the scaffolding must be routinely inspected by a competent supervisor to ensure compliance with safety standards and structural integrity.

4. **Emergency Planning**:
   - Establish an incident response plan for scenarios such as scaffold collapse or worker falls, ensuring first aid-trained personnel are always on-site.
   - Clear evacuation routes must be defined and communicated to all workers.

By implementing the identified preventive measures and recommendations, the risks associated with scaffolding assembly and disassembly can be reduced significantly, creating a safer working environment. Proper adherence to manufacturer guidelines and safety protocols will ensure scaffolding remains functional and hazard-free.""", "B": """### Job Safety Analysis (JSA) Report: Scaffolding Assembly and Disassembly  \n\n#### **Scope of Work**  \nThis report outlines the Job Safety Analysis (JSA) for the assembly and disassembly of scaffolding at the construction site. The task involves ensuring scaffolding is erected and dismantled safely, securely, and in compliance with safety regulations. The analysis identifies hazards, assesses risks, and provides preventive measures to mitigate high and moderate-risk hazards.\n\n---\n\n### **JSA Table: Scaffolding Assembly and Disassembly**\n\n| **Job Step**                          | **Hazard**                                                                 | **Likelihood** | **Impact** | **Preventive Measure**                                                                                     |\n|---------------------------------------|-----------------------------------------------------------------------------|----------------|------------|-----------------------------------------------------------------------------------------------------------|\n| **Site Inspection and Preparation**   | Uneven or unstable ground may cause scaffolding to collapse.               | P5 (Likely)    | C5 (Major) | Level the ground, use base plates with adjustable legs, and compact loose soil.                           |\n|                                       | Presence of debris or obstructions could lead to trips, slips, or falls.   | P5 (Likely)    | C3 (Moderate) | Clear debris and implement a housekeeping policy.                                                         |\n| **Material Inspection**               | Damaged or defective components may fail during use.                       | P4 (Possible)  | C5 (Major) | Inspect components, replace damaged parts, and maintain inspection logs.                                  |\n|                                       | Missing parts could compromise the integrity of the scaffolding.           | P4 (Possible)  | C4 (Significant) | Conduct pre-assembly inventory checks and use manufacturer-approved parts.                                |\n| **Base Setup**                        | Improper placement of base plates or screw jacks may result in instability. | P5 (Likely)    | C5 (Major) | Train workers, use a spirit level, and ensure proper placement of base plates.                            |\n| **Erect the First Level**             | Incorrect assembly of vertical frames and braces may lead to failure.      | P4 (Possible)  | C5 (Major) | Provide detailed instructions, assign experienced personnel, and conduct periodic checks.                 |\n| **Add Subsequent Levels**             | Risk of falls from height while assembling higher levels.                  | P5 (Likely)    | C5 (Major) | Use fall arrest systems, install temporary guardrails, and provide proper access equipment.               |\n| **Install Guardrails and Toe Boards** | Failure to secure guardrails and toe boards may result in falls or tools dropping. | P4 (Possible)  | C4 (Significant) | Train workers on proper installation and conduct final inspections.                                       |\n| **Secure the Scaffolding**            | Inadequate anchoring could cause the scaffolding to collapse.              | P4 (Possible)  | C5 (Major) | Follow manufacturer guidelines, use appropriate ties, and inspect anchors regularly.                      |\n| **Final Inspection**                  | Overlooking defects or improper assembly during inspection.                | P4 (Possible)  | C5 (Major) | Assign qualified inspectors, use checklists, and tag scaffolding as safe only after inspection.           |\n| **Pre-Disassembly Inspection**        | Unstable scaffolding may collapse during disassembly.                      | P4 (Possible)  | C5 (Major) | Disassemble in reverse order, ensure stability, and assign a supervisor.                                  |\n| **Remove Guardrails and Toe Boards**  | Workers may be exposed to fall hazards during removal.                     | P5 (Likely)    | C5 (Major) | Use fall arrest systems and remove guardrails only when ready to disassemble platforms.                   |\n| **Dismantle Platforms**               | Risk of falling planks or platforms during removal.                        | P4 (Possible)  | C5 (Major) | Use hoists or ropes to lower planks safely and clear workers below.                                       |\n| **Disassemble Frames and Braces**     | Improper handling of frames and braces could lead to falling components.   | P4 (Possible)  | C5 (Major) | Train workers on handling techniques and use taglines to guide components safely.                         |\n| **Remove Base Plates**                | Premature removal of base plates may destabilize the structure.            | P3 (Unlikely)  | C5 (Major) | Remove base plates only after dismantling upper levels and monitor stability.                             |\n| **Inspect and Store Materials**       | Damaged components may go unnoticed and be reused.                         | P4 (Possible)  | C4 (Significant) | Inspect components during disassembly, tag damaged parts, and remove them from service.                  |\n| **Site Cleanup**                      | Leftover debris or materials may cause trips or injuries.                  | P5 (Likely)    | C3 (Moderate) | Conduct a final site cleanup and dispose of debris in designated bins.                                    |\n| **Weather-Related Hazards**           | High winds during assembly or disassembly.                                 | P3 (Unlikely)  | C5 (Major) | Monitor weather forecasts, suspend work during high winds, and secure components.                        |\n|                                       | Rain causing slippery surfaces.                                            | P4 (Possible)  | C4 (Significant) | Use slip-resistant mats and provide workers with slip-resistant footwear.                                 |\n|                                       | Extreme heat leading to worker fatigue and errors.                         | P4 (Possible)  | C3 (Moderate) | Schedule work during cooler hours, provide shaded rest areas, and ensure hydration.                       |\n\n---\n\n### **Summary of Findings and Recommendations**  \n\nThe JSA process identified several high and moderate-risk hazards associated with scaffolding assembly and disassembly. Key findings include:  \n- **High-Risk Hazards:** Falls from height, structural instability due to improper assembly or disassembly, and falling objects.  \n- **Moderate-Risk Hazards:** Slips, trips, and falls due to debris or slippery surfaces, and worker fatigue in extreme heat.  \n\n#### **Recommendations:**  \n1. **Training and Supervision:**  \n   - Provide comprehensive training on scaffolding assembly and disassembly techniques.  \n   - Assign experienced supervisors to oversee critical phases of the process.  \n\n2. **Use of PPE and Safety Equipment:**  \n   - Ensure all workers use appropriate PPE, including fall arrest systems, hard hats, and slip-resistant footwear.  \n   - Install temporary guardrails and safety nets during assembly.  \n\n3. **Inspection and Maintenance:**  \n   - Conduct thorough inspections of scaffolding components before and after use.  \n   - Replace damaged or defective parts immediately and maintain inspection logs.  \n\n4. **Site Preparation and Cleanup:**  \n   - Level the ground and clear debris before starting assembly.  \n   - Implement a housekeeping policy to maintain a clean and safe work environment.  \n\n5. **Weather Monitoring:**  \n   - Monitor weather conditions and suspend work during high winds or heavy rain.  \n   - Provide shaded rest areas and hydration stations during extreme heat.  \n\n6. **Communication and Coordination:**  \n   - Establish clear communication protocols to ensure workers are aware of ongoing activities and potential hazards.  \n   - Use a permit-to-work system to authorize and supervise scaffolding activities.  \n\n---\n\n### **Conclusion**  \nThe preventive measures outlined in this report are designed to mitigate the identified hazards and ensure the safety of workers during scaffolding assembly and disassembly. By implementing these measures, the construction team can minimize risks and maintain compliance with safety regulations.\n\nThis report is now complete and ready for dissemination to the construction team and relevant stakeholders. ****"""}
,     {"question": "Tunnel Lining and Support System Installation.", "A": """To conduct a comprehensive Job Safety Analysis (JSA) for "Tunnel Lining and Support System Installation," I will break the task into detailed steps, identify potential hazards, assess their risks, and determine preventive measures. Finally, a table and detailed report summarizing the findings will be presented. Here is the analysis:

---

### **Job Safety Analysis: Tunnel Lining and Support System Installation**

#### **Project Scope**
The scope of this JSA is the installation of a tunnel lining and support system, a critical step in underground construction. This process includes assembling pre-fabricated tunnel segments, placing support structures, and ensuring structural integrity. Safety hazards are inherent due to the underground environment, heavy equipment operation, and potential structural instability. The objective is to analyze each job step, identify potential hazards, assess the risks, and implement preventive measures to mitigate high and moderate risks.

---

### **Job Steps, Hazards, and Preventive Measures**

| **Job Step**                                | **Hazard**                                                                                      | **Likelihood (P)** | **Impact (C)** | **Risk Assessment** | **Preventive Measures**                                                                                     |
|---------------------------------------------|-------------------------------------------------------------------------------------------------|--------------------|----------------|---------------------|-------------------------------------------------------------------------------------------------------------|
| **1. Site Preparation/Inspection**          | Uneven surface causing slips, trips, and falls during site preparation.                         | P4: Possible       | C3: Moderate   | Medium              | Conduct detailed site inspections and level the floor. Ensure proper lighting and safe walkways.            |
|                                             | Existence of hazardous gases in the tunnel.                                                    | P3: Unlikely       | C4: Significant| Medium              | Conduct gas monitoring and ventilation system checks before accessing the tunnel. Install gas detectors.    |
| **2. Delivery of Lining Materials**         | Accidents involving material transport and heavy equipment.                                     | P5: Likely         | C4: Significant| High                | Train operators, use spotters, maintain equipment, and enforce strict traffic management.                   |
|                                             | Falling or shifting loads during unloading.                                                    | P4: Possible       | C4: Significant| Medium              | Use properly rated lifting equipment. Secure loads with rigging and train workers on material handling.     |
| **3. Assembling Tunnel Lining**             | Workers caught between tunnel segments during alignment.                                        | P3: Unlikely       | C5: Major      | High                | Use mechanical guides, maintain communication among workers, and enforce exclusion zones during alignment.  |
|                                             | Equipment failure (e.g., jacks or cranes) causing dropped loads or material collapse.           | P4: Possible       | C4: Significant| Medium              | Inspect and maintain lifting equipment regularly. Train personnel in emergency response procedures.         |
| **4. Installation of Support System**       | Overhead hazards such as falling debris or material from unsecure structural parts.             | P5: Likely         | C5: Major      | High                | Install protective barriers, use PPE (hard hats), and secure all overhead components firmly.                |
|                                             | Structural collapse (partial or complete) during support system placement.                      | P3: Unlikely       | C6: Catastrophic| High               | Conduct geotechnical surveys, use temporary support systems, and implement detailed engineering controls.   |
| **5. Final Inspection and Testing**         | Electrical hazards from faulty wiring or equipment tested onsite.                               | P3: Unlikely       | C3: Moderate   | Medium              | Use insulated tools, inspect electrical systems before testing, and train workers in electrical safety.     |
|                                             | Failure to identify weak points in lining causing future instability or accidents.              | P4: Possible       | C5: Major      | High                | Conduct detailed quality inspections, involve experienced engineers, and peer review inspection reports.    |

---

### **Summary of Key Findings:**

#### **High-Risk Hazards**
1. **Material Transport Accidents (P5:C4)**: There is a high chance of accidents involving heavy equipment and material transport during tunnel lining delivery.
   - *Preventive Measures*: Train operators, implement traffic controls, and designate unloading areas.
2. **Workers Caught in Tunnel Segments (P3:C5)**: Aligning tunnel segments incorrectly poses a risk of major injuries due to crushing.
   - *Preventive Measures*: Mechanical guides, clear communication protocols, and exclusion zones.
3. **Falling Debris (P5:C5)**: Installation of support systems presents an overhead hazard to workers.
   - *Preventive Measures*: Use protective barriers, wear PPE, and conduct pre-installation inspections.
4. **Structural Collapse (P3:C6)**: Support system failure or uneven load distribution poses catastrophic risks.
   - *Preventive Measures*: Conduct geotechnical surveys, follow strict engineering designs, and use temporary support systems.
5. **Weak Point Identification (P4:C5)**: Undetected weak points in the tunnel lining could lead to future accidents.
   - *Preventive Measures*: Implement rigorous quality inspections and engage expert engineers.

#### **Moderate-Risk Hazards**
1. **Slips, Trips, and Falls (P4:C3)**: An uneven underground surface increases the likelihood of minor or moderate injuries.
   - *Preventive Measures*: Level the floor, ensure walkways are clear, and improve lighting.
2. **Hazardous Gases (P3:C4)**: Presence of hazardous gases inside tunnels may pose short-term or long-term health risks.
   - *Preventive Measures*: Use gas detectors, ensure proper ventilation systems, and regularly test air quality.
3. **Falling or Shifting Materials (P4:C4)**: During unloading or handling, materials may drop, injuring workers.
   - *Preventive Measures*: Use appropriate equipment and provide training for material handling.

---

### **Recommendations and Conclusion**

The **Tunnel Lining and Support System Installation** process involves several high and moderate risks, mainly related to overhead hazards, crushing injuries, material handling, and structural integrity. High-priority actions include:
- Training workers on equipment operation, emergency response, and safe practices.
- Implementing rigorous inspection protocols for lifting and installation equipment.
- Ensuring structural stability through thorough engineering checks and temporary supports.
- Deploying proper PPE such as helmets, gloves, and safety boots to address personal safety in the workplace.

By implementing the proposed preventive measures, the likelihood and impact of identified hazards can be significantly reduced, creating a safer working environment. It is essential to enforce these safety standards rigorously and maintain continuous hazard assessments throughout the project to account for dynamic risks.

--- 

### **Appendix: Risk Matrix Definitions**

The risk matrix categorizes risk by combining likelihood (P) and impact (C):
- **High Risk (H)**: Immediate corrective measures required.
- **Medium Risk (M)**: Mitigate as soon as possible.
- **Low Risk (L)**: Manage through routine procedures.""", "B": """**Comprehensive Job Safety Analysis (JSA) Report for Tunnel Lining and Support System Installation**\n\n---\n\n### **Structured Table of Job Steps, Hazards, Risk Assessments, and Preventive Measures**\n\n| **Job Step**                     | **Hazard**                                                                 | **Likelihood (P)** | **Impact (C)** | **Preventive Measures**                                                                                     |\n|-----------------------------------|-----------------------------------------------------------------------------|---------------------|----------------|-------------------------------------------------------------------------------------------------------------|\n| **Site Preparation**              | Falling debris or loose rocks                                              | P5 (Likely)         | C4 (Significant) | Conduct pre-inspection, install protective barriers, mandate PPE use.                                       |\n|                                   | Inadequate ventilation                                                     | P5 (Likely)         | C3 (Moderate)   | Install temporary ventilation, monitor air quality, provide respiratory protection.                         |\n|                                   | Insufficient lighting                                                      | P3 (Unlikely)       | C3 (Moderate)   | Install temporary lighting, use portable lights, inspect lighting equipment regularly.                      |\n| **Surface Preparation**           | Dust and debris exposure                                                   | P5 (Likely)         | C3 (Moderate)   | Use dust suppression systems, provide respiratory protection, limit exposure time.                          |\n|                                   | Slips, trips, or falls                                                     | P4 (Possible)       | C3 (Moderate)   | Clean and dry surfaces, mark uneven areas, require slip-resistant footwear.                                 |\n|                                   | Structural instability in weak zones                                       | P4 (Possible)       | C5 (Major)      | Conduct geotechnical survey, install temporary supports, restrict access to unstable areas.                 |\n| **Material Delivery and Staging** | Improper handling of heavy materials                                       | P5 (Likely)         | C4 (Significant) | Train workers, use mechanical aids, inspect lifting equipment.                                              |\n|                                   | Obstructions in staging area                                               | P5 (Likely)         | C3 (Moderate)   | Designate staging areas, conduct housekeeping, mark walkways clearly.                                       |\n| **Primary Support Installation**  | Falling objects during installation                                        | P4 (Possible)       | C4 (Significant) | Use tool lanyards, install overhead protection, restrict access below active zones.                         |\n|                                   | High-pressure equipment exposure                                           | P4 (Possible)       | C4 (Significant) | Train workers, maintain equipment, provide PPE.                                                             |\n|                                   | Entanglement with wire mesh                                                | P4 (Possible)       | C3 (Moderate)   | Use proper handling techniques, provide cut-resistant gloves, ensure adequate spacing.                      |\n| **Lining Installation**           | Misalignment of lining sections                                            | P4 (Possible)       | C5 (Major)      | Use laser alignment tools, conduct quality checks, train workers.                                           |\n|                                   | Falling objects during installation                                        | P4 (Possible)       | C4 (Significant) | Secure materials, use guardrails, restrict access below active zones.                                       |\n|                                   | Chemical exposure from grout/sealant                                       | P4 (Possible)       | C3 (Moderate)   | Use low-toxicity materials, provide PPE, ensure proper ventilation.                                         |\n| **Secondary Support Installation**| Injury from handling heavy structures                                      | P4 (Possible)       | C4 (Significant) | Use mechanical aids, train workers, inspect equipment.                                                     |\n|                                   | Misalignment or improper fastening                                         | P4 (Possible)       | C5 (Major)      | Use alignment tools, conduct quality checks, train workers.                                                 |\n| **Quality Control and Inspection**| Radiation exposure during testing                                          | P4 (Possible)       | C4 (Significant) | Use shielding, train workers, limit access to testing areas.                                                |\n|                                   | Falls during inspection                                                    | P4 (Possible)       | C3 (Moderate)   | Use fall protection systems, ensure stable walkways, train workers.                                         |\n| **Final Surface Treatment**       | Chemical exposure from coatings                                            | P5 (Likely)         | C3 (Moderate)   | Use low-toxicity materials, provide PPE, ensure proper ventilation.                                         |\n|                                   | Slips or falls during treatment                                            | P4 (Possible)       | C3 (Moderate)   | Use slip-resistant mats, mark wet areas, provide slip-resistant footwear.                                   |\n| **Site Cleanup and Demobilization**| Injury from waste handling                                                 | P4 (Possible)       | C3 (Moderate)   | Train workers, use mechanical aids, provide PPE.                                                            |\n|                                   | Environmental contamination                                                | P4 (Possible)       | C4 (Significant) | Implement waste management plan, conduct audits, train workers on compliance.                               |\n| **Handover and Documentation**    | Incomplete documentation                                                   | P4 (Possible)       | C3 (Moderate)   | Use standardized templates, conduct final reviews, train workers.                                           |\n|                                   | Miscommunication during walkthrough                                        | P4 (Possible)       | C3 (Moderate)   | Use detailed checklists, assign a point of contact, document findings and agreements.                       |\n\n---\n\n### **Summary of Findings and Recommendations**\n\nThe Job Safety Analysis (JSA) for the Tunnel Lining and Support System Installation identified several high and moderate-risk hazards across all job steps. The most critical risks include falling debris, structural instability, misalignment of lining sections, and chemical exposure. These hazards have the potential to cause significant injuries, fatalities, or environmental damage if not properly managed.\n\n**Key Recommendations:**\n1. **Prevention of Falling Hazards:**\n   - Install protective barriers and overhead protection in high-risk areas.\n   - Mandate the use of PPE, such as hard hats and safety harnesses, for all workers.\n\n2. **Ventilation and Air Quality:**\n   - Ensure adequate ventilation systems are in place and monitor air quality regularly.\n   - Provide respiratory protection to workers in areas with poor air quality or chemical exposure.\n\n3. **Training and Equipment Maintenance:**\n   - Conduct regular training sessions for workers on safe handling techniques, equipment operation, and hazard awareness.\n   - Implement a strict maintenance schedule for all equipment to prevent malfunctions.\n\n4. **Quality Control and Alignment:**\n   - Use precision tools, such as laser alignment systems, to ensure proper installation of lining and support structures.\n   - Conduct frequent quality checks to identify and address issues promptly.\n\n5. **Waste Management and Environmental Compliance:**\n   - Develop and enforce a waste management plan that complies with environmental regulations.\n   - Train workers on proper waste handling and disposal procedures to prevent contamination.\n\n6. **Documentation and Communication:**\n   - Use standardized templates and checklists to ensure all documentation is complete and accurate.\n   - Assign a dedicated point of contact to facilitate clear communication during the final walkthrough.\n\n**Conclusion:**\nBy implementing the preventive measures outlined in this report, the risks associated with the Tunnel Lining and Support System Installation can be effectively mitigated. It is essential to maintain a proactive approach to safety management, with regular training, inspections, and reviews to ensure compliance with safety standards and regulations.\n\n---\n\n**Next Step:** Distribute this report to all relevant stakeholders, including the project team, for implementation and monitoring of the recommended preventive measures.\n\n****"""
}]

# Setting the page to wide mode
st.set_page_config(layout="wide")

def extract_tables(markdown_text):
    """
    Extracts tables from Markdown text and returns them as a list of DataFrames.
    """
    tables = []
    pattern = re.compile(r'(\|.+?\|(?:\n\|[-:]+)+\n(?:\|.*?\|(?:\n|$))+)', re.DOTALL)
    matches = pattern.findall(markdown_text)
    for match in matches:
        table = pd.read_csv(StringIO(match), sep='|').dropna(axis=1, how='all').dropna(axis=0, how='all')
        tables.append(table)
    return tables

def display_response(response_text):
    """
    Displays the response text, rendering Markdown and tables appropriately.
    """
    tables = extract_tables(response_text)
    for table in tables:
        st.table(table)
        response_text = response_text.replace(table.to_markdown(), '')

    st.markdown(response_text)

def log_to_google_sheet(selection, model, question, task):
    try:
        """
        Logs the user's selection to Google Sheets.
        """
        # Check if running locally or on Streamlit Cloud
        if os.path.exists("credentials.json"):
            # Load credentials locally
            with open("credentials.json") as f:
                service_account_info = json.load(f)
        else:
            # Load credentials from Streamlit Cloud's st.secrets
            service_account_info = st.secrets["gcp_service_account"]

        # Authenticate with Google Sheets API
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        # Use gspread to access Google Sheets
        client = gspread.authorize(credentials)

        # Open your Google Sheet by name
        
        sheet = client.open_by_key("1Fn7mX6JsvKqJEammSZbtE_s_RJCmzQfjK8KBXQr2ZEM").sheet1

        # Add a new row with the data
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([current_time, task, selection, model, question])
    except Exception as e:
        st.error(f"Failed to log response to Google Sheets: {e}")

st.title("LLM Response Comparison")

# Show both options at the start
st.header("Choose a Task")
# st.header("Choose a Task or Input Your Task")

# # Display task buttons
# st.subheader("Choose from Predefined Tasks")

col1, col2, col3, col4, col5 = st.columns(5)

# Initialize session state variables
if "response_mapping" not in st.session_state:
    st.session_state.response_mapping = {"A": "", "B": ""}
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""
if "final_mapping" not in st.session_state:
    st.session_state.final_mapping = None
if "responses_shuffled" not in st.session_state:
    st.session_state.responses_shuffled = False
if "selection_made" not in st.session_state:
    st.session_state.selection_made = False

# Handle predefined task button presses
if col1.button(initial_questions[0]["question"]):
    st.session_state.current_question = initial_questions[0]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False
if col2.button(initial_questions[1]["question"]):
    st.session_state.current_question = initial_questions[1]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False
if col3.button(initial_questions[2]["question"]):
    st.session_state.current_question = initial_questions[2]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False
if col4.button(initial_questions[3]["question"]):
    st.session_state.current_question = initial_questions[3]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False
if col5.button(initial_questions[4]["question"]):
    st.session_state.current_question = initial_questions[4]
    st.session_state.user_prompt = ""
    st.session_state.responses_shuffled = False
    st.session_state.selection_made = False

# Randomize responses if a question is selected and responses are not shuffled
if st.session_state.current_question and not st.session_state.responses_shuffled:
    original_mapping = {
        "Model 1": st.session_state.current_question["A"],
        "Model 2": st.session_state.current_question["B"]
    }

    shuffled = list(original_mapping.items())
    random.shuffle(shuffled)
    st.session_state.response_mapping = {
        "A": {"response": shuffled[0][1], "model": shuffled[0][0]},
        "B": {"response": shuffled[1][1], "model": shuffled[1][0]}
    }
    st.session_state.final_mapping = st.session_state.response_mapping.copy()
    st.session_state.responses_shuffled = True

# Handle custom task input

# st.subheader("Option 2: Enter your task")
# st.session_state.user_prompt = st.text_input("", st.session_state.user_prompt)
# if st.session_state.user_prompt:
#     if not st.session_state.responses_shuffled:
#         shuffled = [
#             {"response": f"Generated response for A based on: {st.session_state.user_prompt}", "model": "Model 1"},
#             {"response": f"Generated response for B based on: {st.session_state.user_prompt}", "model": "Model 2"}
#         ]
#         random.shuffle(shuffled)
#         st.session_state.response_mapping = {
#             "A": shuffled[0],
#             "B": shuffled[1]
#         }
#         st.session_state.final_mapping = st.session_state.response_mapping.copy()
#         st.session_state.responses_shuffled = True

# Display responses if available
if st.session_state.final_mapping and st.session_state.final_mapping["A"] and st.session_state.final_mapping["B"]:
    st.subheader("Choose the Better LLM Response")
    with st.form("response_form"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.subheader("Response A")
            display_response(st.session_state.final_mapping["A"]["response"])

        with col2:
            st.subheader("Response B")
            display_response(st.session_state.final_mapping["B"]["response"])

        # User interaction buttons
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            a_better = st.form_submit_button("👈 A is better")
        with col_b2:
            b_better = st.form_submit_button("👉 B is better")
        with col_b3:
            tie = st.form_submit_button("🤝 Tie")
        with col_b4:
            both_bad = st.form_submit_button("👎 Both are bad")

        # Display the user selection result and map back to the model
        if not st.session_state.selection_made:
            if a_better:
                log_to_google_sheet("A is better", st.session_state.final_mapping['A']['model'], st.session_state.current_question['question'], st.session_state.user_prompt)
                st.session_state.selection_made = True
                st.success(f"You selected: A is better")
            elif b_better:
                log_to_google_sheet("B is better", st.session_state.final_mapping['B']['model'], st.session_state.current_question['question'], st.session_state.user_prompt)
                st.session_state.selection_made = True
                st.success(f"You selected: B is better")
            elif tie:
                log_to_google_sheet("Tie", "Model 1 and Model 2", st.session_state.current_question['question'], st.session_state.user_prompt)
                st.session_state.selection_made = True
                st.success("You selected: It's a tie")
            elif both_bad:
                log_to_google_sheet("Both are bad", "None", st.session_state.current_question['question'], st.session_state.user_prompt)
                st.session_state.selection_made = True
                st.success("You selected: Both are bad")
