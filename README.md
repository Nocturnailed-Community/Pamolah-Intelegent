# **Team Name**
Pamolah Intelegent

## **Project Title**
DEEP DENTAL: Analisis Digital untuk Mendeteksi Penyakit Gigi dengan Model Deep Learning

## **Authors**
- Muhammad Ikhwan Fathulloh (UTB)
- M. Hasanudin (UTB)
- Firgiawan Faira (UTB)

## **Background**
- The rapid development of technology, particularly in AI, has significant implications for dental health.
- Poor dental health can lead to systemic diseases, affecting overall health.
- WHO reports indicate that nearly 3.5 billion people suffer from dental health issues globally.
- In Indonesia, only 11.2% of individuals with dental problems seek medical care, highlighting a need for better education and access to dental health services.

## **Objectives and Benefits**
### **Objectives**
1. **Early Diagnosis**: Develop an AI model to analyze dental conditions using digital image datasets and patient complaints.
2. **Treatment Recommendations**: Provide appropriate initial care recommendations based on detected conditions.
3. **Public Awareness**: Serve as an educational platform to improve dental health awareness.
4. **Health Monitoring**: Track users' dental health history for better management.

### **Benefits**
- **For Society**: Improved access to affordable diagnosis and increased awareness of healthy living.
- **For Healthcare Industry**: Enhanced dental services and patient management efficiency.
- **For Government**: Data for public health policy planning and improved healthcare access.
- **For Education**: Advancement in research and education for dental students.

## **Methodology**
### **Model Development**
- **Computer Vision (CNN)**: For image analysis of dental conditions.
- **Natural Language Processing (NLP)**: Using BERT to analyze patient complaints.

### **Algorithms Used**
1. **Image Analysis (CNN)**
   - Architecture: ResNet-50 or EfficientNet.
   - Classes: Normal, Caries, Gingivitis, Dental Plaque, Abscess.
   - Preprocessing: Data augmentation, normalization, resizing.
   - Optimization: Adam optimizer, categorical crossentropy loss.

2. **Complaint Analysis (NLP - BERT)**
   - Architecture: Pre-trained BERT with additional classification layer.
   - Preprocessing: Tokenization, padding, and truncation.
   - Optimization: AdamW optimizer, crossentropy loss.

## **Implementation Steps**
1. **Image Analysis with CNN**
   - Data preparation and augmentation.
   - Model training and evaluation.

2. **Complaint Analysis with BERT**
   - Text preprocessing and model training.

3. **Integration of CNN and BERT**
   - Combine outputs for comprehensive diagnosis.

4. **Deployment**
   - API development using Flask.
   - Model serving on cloud platforms.

## **Technology Stack**
- **Model Development**: Google Colaboratory, BLIV, Vertex AI.
- **Data Storage**: MySQL, Google Cloud Storage.
- **Deployment**: Docker, Google Cloud Run.
- **Frontend**: Flutter for mobile application.

## **Datasets**
### **Computer Vision Datasets**
- **Normal Dataset**: Baseline for normal dental conditions.
- **Caries Dataset**: For detecting tooth decay.
- **Gingivitis Dataset**: For detecting gum inflammation.
- **Dental Plaque Dataset**: For detecting plaque.
- **Abscess Dataset**: For detecting dental abscesses.

### **NLP Datasets**
- **N2C2 Dataset**: Clinical notes for text classification.
- **PMC Open Access Subset**: Medical articles for text analysis.

## **Future Work**
- Further research and development in digital health solutions for dental care.
- Expansion of educational resources for the public.

## **References**
1. R. B. Rahman et al., "A comprehensive dental dataset of six classes for deep learning based object detection study," Data Br., 2024.
2. S. Bhat et al., "A comprehensive survey of deep learning algorithms and applications in dental radiograph analysis," Healthc. Anal., 2023.
3. World Health Organization, Global oral health status report, 2022.
4. Kemenkes RI, "Survei Kesehatan Indonesia 2023 (SKI)," Kemenkes, 2023.

## **Contact**
For more information, please visit the [GitHub Repository](https://github.com/your-repo-link).

---

This README provides a comprehensive overview of the DEEP DENTAL project, its objectives, methodologies, and future directions.