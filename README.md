# OutBoxers - Smart Conveyor Belt System  

Welcome to **OutBoxers**, our innovative solution developed during the Lauzhack hackathon for BOBST. This project combines hardware, software, and cloud integration to create an intelligent conveyor belt system capable of detecting, sorting, and analyzing box production in real time.  

---

## System Overview  

### Hardware Functionality  

- **Adjustable Conveyor Belt Speed**  
  The conveyor belt's speed is regulated using a rotary encoder, allowing dynamic adjustment to match production requirements.  

- **Defect Detection at the Start of the Conveyor**  
  An **ultrasonic sensor** is positioned at the start of the belt to detect any irregularities in the boxes, such as incorrect dimensions or improper placement.  

- **Error Detection at the End of the Conveyor**  
  An **infrared sensor** at the end of the conveyor identifies potential issues during transportation, such as misaligned or stuck boxes.  

- **Defective Box Diverter**  
  If a box is identified as defective by the sensors, a **box diverter mechanism** reroutes it to a separate path at the end of the conveyor, ensuring smooth operation for non-defective boxes.  

- **Current Consumption Monitoring**  
  A **current sensor** monitors the power consumption of the conveyor system, enabling real-time insights into energy efficiency and operational costs.  

---

## Software Functionality  

- **Multithreading for Sensor and Motor Management**  
  The software uses **multithreading** to manage sensors and motors in parallel, ensuring real-time control and responsiveness.  

- **Data Collection and Transmission**  
  Key operational data—such as power consumption, production rate, and conveyor speed—are collected and sent to **Microsoft Azure** for storage and analysis.  

- **Mobile Application**  
  A **mobile application** allows users to manage shifts, monitor system status, and interact with key performance indicators (KPIs).  

- **Automated Jobs Integration**  
  Integration with **BOBST Connect** enables the execution of automated tasks, streamlining productivity and reducing manual intervention.  

---

## Technical Highlights  

- **Hardware:** Rotary encoder, ultrasonic sensor, infrared sensor, current sensor, servo-controlled diverter.  
- **Software:** Python-based multithreading for real-time control, Azure integration for data logging, mobile app for management.  
- **Cloud Integration:** Microsoft Azure for storing and analyzing system metrics.  
- **Application Scope:** Operational insights, defect management, production reporting, and energy monitoring.  

---

## Future Enhancements  

While we are proud of what we accomplished during the hackathon, there were additional ideas we could not implement due to time constraints:  

1. **Predictive Maintenance**  
   - Using sensor and motor data to anticipate mechanical failures or identify wear and tear early.  

2. **Enhanced Connectivity with Mobile Application**  
   - Real-time control of the conveyor belt and alert management directly from the mobile application.  

3. **Advanced Alarm System**  
   - Integration of a robust alert system with the mobile app for instant notifications and quick issue resolution.  

---

## How It Works  

1. Boxes enter the conveyor belt, and their dimensions and positioning are analyzed by the ultrasonic sensor.  
2. Boxes with detected defects are flagged for redirection.  
3. As the box progresses, an infrared sensor checks for additional errors at the end of the line.  
4. If the box is marked as defective, the diverter mechanism separates it from the normal production flow.  
5. The system continuously tracks speed, energy usage, and defect counts, sending this data to the cloud.  
6. The mobile app and automated job scheduler provide additional layers of control and operational insight.  

---

## Future Potential  

The OutBoxers system is scalable and modular, making it an ideal solution for modern industrial applications. With additional sensors or advanced AI integration, it can adapt to more complex scenarios and higher production volumes.  

We hope this project inspires further innovation in smart manufacturing!  

---

🎉 **Thank you for supporting our hackathon journey!** 🎉  
