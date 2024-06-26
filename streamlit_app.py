#Research & Development App - OS Natural Language Interface

#Import for supporting ChromaDB vector database
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

#Modules
import streamlit as st
import os
import google.generativeai as ggi
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema.runnable import RunnableMap
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.prompts import ChatPromptTemplate

#Variables to hold our different documents to be used.
fileTroy = "RAGDocuments/prompt_answer.csv"
fileOS = "RAGDocuments/prompt_OS_answer.csv"

#Get API Key from Secrets file into a variable.
apikey = st.secrets["API_KEY"]

#A function to load a document.
def DocLoader(fileName):
   loader = CSVLoader(fileName, csv_args={'delimiter':','})
   return loader.load()

#A function to split a document.
#Chunking sizes chosen should cover entire lines and overlap parts of contiguous lines
def DocSplitter(document):
   splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=200)
   return splitter.split_documents(document)

# Commented due to streamlit community cloud now giving file errors. I will use again once I have resolved the file reading issues.
#Load our documents used for RAG
#loadedTroy = DocLoader(fileTroy)
#loadedOS = DocLoader(fileOS)
#Split our documents
#troy_Split = DocSplitter(loadedTroy)
#OS_Split = DocSplitter(loadedOS)
#Use Troy csv chunks and embeddings to create vectorDB
#vector_index = Chroma.from_documents(troy_Split, embeddings).as_retriever(search_kwargs={"k":5})
#lcGemini = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=apikey,temperature=0.9,
#                                  convert_system_message_to_human=True)

#Create an embeddings object.
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=apikey)

#I am inlining the CSV text. StreamLit Community Cloud stopped seeing my files. I will find the issue and resolve it.
vectorstore = DocArrayInMemorySearch.from_texts(
["Hi	How can I help you?",
"What CS degrees does your university university offer?	Our university offers BS in Computer Science, BS in Applied Computer Science, BS in Cyber Security, MS in Computer Science.,",
"What is the difference between Computer Science and Applied Computer Science?	Computer Science focuses on the theoretical foundations of computing while Applied Computer Science focuses on the practical applications of computing in various fields.,",
"What kind of jobs can I get with a degree in Applied Computer Science?	Graduates with a degree in Applied Computer Science can work as software developers, network and systems administrators, database administrators, web developers, data analysts, IT project managers, and more.,",
"Is programming experience required to apply for the program?	While some programming experience is helpful, it is not required to apply for the program. The program curriculum includes introductory programming courses to help students build a strong foundation in coding.,",
"Can I complete the program entirely online?	Yes, the program offers online courses for students who prefer to learn remotely.   ,",
"What kind of computer hardware and software will I need for the program?	The program requires a computer with internet access and basic software such as a word processor and a web browser. Specific software requirements may vary depending on the courses you take.,",
"What is computer science? 	Computer science is the study of computers and computational systems, including their theory, design, development, and application.,",
"What kind of jobs can I get with a degree in computer science? 	Computer science graduates can pursue a wide range of career paths, including software development, database administration, cybersecurity, network architecture, artificial intelligence, and more.,",
"Do I need to have prior programming experience to study computer science? 	No. While some programming experience is helpful, it is not required to apply for the program. The program curriculum includes introductory programming courses to help students build a strong foundation in coding.,",
"What kind of software/hardware will I be working with? 	Depending on the program, you may be working with a variety of software and hardware, including programming languages like C++,  Java or Python, database management systems, virtual machines, cloud computing platforms, and more.,",
"What kind of job and internship opportunities are available to computer science students? 	Computer science students have a wide range of job and internship opportunities, including positions at tech startups, large corporations, government agencies, non-profits, and more. The program has a strong record of preparing students for successful careers in the field.,",
"Can I study computer science online? 	Yes, Our university offers the online computer science program, which can be a flexible and convenient option for students who need to balance their studies with work or other responsibilities.,",
"What is the job placement rate for graduates of the program?	The job placement rate for graduates of the program varies depending on various factors such as location, industry, and individual qualifications. However, the program has a strong record of preparing students for successful careers in the field.,",
"Can I pursue a Cyber Security degree online, or is it only offered on campus? 	Yes, Our university offers both online and on campus programs, so you may have the option to choose which format works best for you. ,",
"What kind of coursework can I expect in the Cyber Security program? 	Coursework covers a wide range of topics, including network security, digital forensics, cryptography, secure programming, and more. ,",
"Does the program offer any hands-on experience or internships? 	Yes, the program offers hands-on experience through lab courses or projects. These experiences can be valuable for building real-world skills and gaining practical experience in the field.The program also offers internship opportunities. We recommend students for internships for several public and private companies. Some of the companies who have been taking interns from us on a regular basis include medicare, CGI, Alfa Insurance, IRS. ,",
"What kind of jobs can I get with a Cyber Security degree? 	Graduates of the Cyber Security program may be qualified for a variety of roles in the field, including cybersecurity analyst, network security engineer, information security manager, digital forensics analyst, and more. The specific job titles and responsibilities may vary depending on the individual's interests and experience level.,",
"What kind of support is available for students who need help with the coursework or assignments? 	Our university offers academic support services such as tutoring, writing centers, and career services. Students may also be able to seek assistance from their instructors or peers through online discussion boards or other communication channels. ,",
"Is CS master program available online? 	Yes, the program is available online for students who prefer a flexible schedule.,",
"What career opportunities are available after completing the Master program? 	Depending on your concentration, graduates can pursue careers such as data scientist, network security engineer, software developer, game designer, and many more.,",
"What is the job outlook for the computer science field?	According to the Bureau of Labor Statistics, employment of computer and information technology occupations is projected to grow 11 percent from 2019 to 2029, much faster than the average for all occupations. This means that there will be a continued demand for computer science professionals in various industries.,",
"Can I speak with a faculty member or current student about the program? 	Yes, you can contact the program's department or check the program's website for information on how to schedule a meeting with a faculty member or current student.,",
"What is the application deadline?	The application deadline is on a rolling basis, meaning applications are reviewed and accepted continuously until all available positions are filled.,",
"What are the admission requirements?	Please check the link https://www.troy.edu/applications-admissions/admissions-process-requirements/undergraduate/index.html,",
"How do I reach the department for more details?	Yes, you can contact the department at https://www.troy.edu/academics/colleges-schools/college-arts-sciences/departments/school-science-technology/computer-science/faculty-staff.html,",
"What programs or concentrations do you have in MS Computer Science?	Please check the link: https://www.troy.edu/academics/academic-programs/graduate/computer-science.html?actualpro=Computer%20Science%20-%20Artificial%20Intelligence%20%28Non-Thesis%29,",
"What are in applied computer science?	Please check: https://www.troy.edu/academics/academic-programs/applied-computer-science.html,",
"What are in BS computer science? 	Please check: https://www.troy.edu/academics/academic-programs/bachelors-degree-in-computer-science.html,",
"What are in BS cybersecurity? 	Please check: https://www.troy.edu/academics/academic-programs/cyber-security.html,",
"what is the tuition?	Please check: https://www.troy.edu/scholarships-costs-aid/costs/tuition-fees/index.html,",
"what is BS Computer Science curriculum or requirement	Please check: https://www.troy.edu/academics/catalogs/undergraduate-catalog/arts-and-sciences.html#ComputerScienceProgram,",
"what is BS Applied Computer Science curriculum or requirement	Please check: https://www.troy.edu/academics/catalogs/undergraduate-catalog/arts-and-sciences.html#ComputerScienceAppliedMajor,",
"what is BS cyber security curriculum or requirement	Please check: https://www.troy.edu/academics/catalogs/undergraduate-catalog/arts-and-sciences.html#CyberSecurityProgram,",
"what is MS Computer Science curriculum or requirement	Please check: https://www.troy.edu/academics/catalogs/graduate-catalog/college-arts-sciences.html#Master-Science-Computer-Science,",
"what is the undergraduate admission requirements	Please check: https://www.troy.edu/applications-admissions/admissions-process-requirements/undergraduate/index.html,",
"what is the graduate admission requirements	please check: https://www.troy.edu/applications-admissions/admissions-process-requirements/graduate/index.html,",
"what is international student admission requirements	please check: https://www.troy.edu/applications-admissions/admissions-process-requirements/international-student/index.html,",
"what is the admission requirements	please check: https://www.troy.edu/applications-admissions/index.html?campaign=19100766843&content=638525310699&keyword=apply%20troy%20university&adgroup=141921234377&location=9011692&adposition=&placement=&network=g&gad_source=1&gclid=CjwKCAjwh4-wBhB3EiwAeJsppPEiLwrCOhLkSBVH0BGDHolb1aIW9Y4c1iIIb7AKKoBk07KrnymW0RoCmHsQAvD_BwE,",
"What are the prerequisites for enrolling in the MS in Computer Science program?	Prerequisites for enrolling in the MS in Computer Science program typically include a bachelor's degree in a related field, such as computer science or engineering, with coursework in  programming, algorithms, and data structures. Please check details in: https://www.troy.edu/academics/catalogs/graduate-catalog/college-arts-sciences.html#Master-Science-Computer-Science,",
"Are there any scholarships available for students in the computer science programs?	There are various scholarships available for students in the computer science programs at Troy University. These scholarships may be based on academic merit, financial need, or specific criteria set by the  university. Please check: https://www.troy.edu/scholarships-costs-aid/scholarships/index.html?campaign=19106840320&content=638648530946&keyword=troy%20university%20scholarships&adgroup=146951721351&location=9011692&adposition=&placement=&network=g&gad_source=1&gclid=CjwKCAjwh4-wBhB3EiwAeJsppLXTAVTK5r7cr3LErweub8EOJmLORlTvBdCXwwauRG8qyjpDOEZqsxoC_XcQAvD_BwE,",
"How long does it typically take to complete the BS in Computer Science?	The typical duration to complete the BS in Computer Science at Troy University is approximately four years for full-time students.,",
"Can you tell me more about the faculty in the Computer Science department?	The Computer Science department at Troy University comprises experienced faculty members who hold advanced degrees in computer science and related fields. They are dedicated to providing high-quality education and mentorship to students. Please check: https://www.troy.edu/academics/colleges-schools/college-arts-sciences/departments/school-science-technology/computer-science/faculty-staff.html,",
"What opportunities are there for undergraduate research in the Computer Science program?	Opportunities for undergraduate research in the Computer Science program include participating in faculty-led research projects, internships, and independent research initiatives.,",
"What is the average class size for computer science courses?	The average class size for computer science courses at Troy University varies depending on the specific course and level.,",
"How does the department support students in finding internships in computer science?	The department supports students in finding internships in computer science through career counseling, internship placement services, networking events, and partnerships with industry professionals and companies.,",
"What are the latest research areas or projects in the Computer Science department?	The latest research areas or projects in the Computer Science department may include artificial intelligence, machine learning, cybersecurity, data science, and computer networking, among others.,",
"Are there any student organizations or clubs related to computer science?	Troy University offers various student organizations and clubs related to computer science, providing opportunities for networking, professional development, and extracurricular activities such as hackathon. ,",
"What are the specific topics covered in the Cyber Security program's coursework?	The Cyber Security program's coursework covers specific topics such as network security, cryptography, ethical hacking, digital forensics, and risk management.,",
"Do computer science students have access to special software or technology labs?	Computer science students at Troy University have access to special software and technology labs equipped with industry-standard tools and resources for hands-on learning and experimentation. We have on-site cybersecurity lab for both on campus and online students. ,",
"Can you explain the differences between the thesis and non-thesis options in the master's program?	The master's program in computer science typically offers both thesis and non-thesis options. The thesis option involves conducting original research and writing a thesis, while the non-thesis option involve additional coursework.,",
"What are the key skills or concepts that the Applied Computer Science program emphasizes?	The Applied Computer Science program emphasizes key skills and concepts such as software development, database management, programming languages, problem-solving, and project management.,",
"How do graduates of the Cyber Security program rate their experience in terms of job readiness?	Graduates of the Cyber Security program from Troy University rate their experience positively in terms of job readiness, as the program equips them with practical skills and knowledge highly valued by employers in the cybersecurity industry.,",
"What partnerships does the Computer Science department have with industry companies?	The Computer Science department at Troy University maintains partnerships with industry companies through internship programs, collaborative research projects, guest lectures, and career placement opportunities.,",
"Are there any capstone projects or practical experiences required for the computer science undergraduate programs?	Capstone projects or practical experiences are typically required for the computer science undergraduate programs at Troy University, providing students with opportunities to apply their skills to real-world projects and challenges.,",
"What programming languages will I learn during the Computer Science program?	Programming languages taught during the Computer Science program may include Java, C++, Python, SQL, JavaScript, and others, depending on the specific courses and curriculum.,",
"How is the curriculum designed to stay current with evolving technology trends?	The curriculum is designed to stay current with evolving technology trends through regular updates, industry input, faculty expertise, and collaboration with professionals and organizations in the field.,",
"Can students from other majors take computer science courses as electives?	Students from other majors may be able to take computer science courses as electives, depending on availability, prerequisites, and approval from the department or academic advisor.,",
"What is the process for transferring into the Computer Science program from another major or school?	The process for transferring into the Computer Science program from another major or school typically involves meeting admission requirements, submitting transcripts, and possibly undergoing a credit evaluation to determine transferable credits. Students are encouraged to consult with the department or admissions office for specific guidance.,",
"Is Troy University's Computer Science program accredited by ABET?	Currently, Troy University's Computer Science program is undergoing the accreditation process with ABET, the recognized accreditor for computing programs. While the accreditation status is pending, Troy University is accredited by the Southern Association of Colleges and Schools Commission on Colleges (SACSCOC) to award associate, baccalaureate, master, educational specialist, and doctoral degrees.,",
"What is the start day of term 5?	Please check academic calendar: https://www.troy.edu/academics/calendar.html,",
"What concentrations are in MS CS 	MS CS offers concentrations in AI, Bioinformatics, Cloud and Big Data, Computer Network and Security, cyber security, data science, software development, video game design,",
"What is a passing grade at Troy University?	1. A candidate for graduation must have an overall C aver- age (2.0 on a 4.0 scale) on Troy University courses. 2. A candidate for graduation must have an overall C cu- mulative average (2.0 on a 4.0 scale).,",
"What is the graduation day at any year	Please check academic calendar: https://www.troy.edu/academics/calendar.html,",
"Who is Dr. Dr. Alberto Arteta, or Dr. Hyung Jae (Chris) Chang or Richard A. Fulton or Dr. Xiaoli Huan or Dr. Byungkwan Jung, or Dr. Suman Kumar or Dr. Long Ma, or Dr. Bill Zhong or Dr. Yanjun Zhao	He is a professor in Troy Computer Science department. Please check the contact information: https://www.troy.edu/academics/colleges-schools/college-arts-sciences/departments/school-science-technology/computer-science/faculty-staff.html",
"How do you shutdown Windows? You use the Windows shutdown command.",
"How do you reboot Windows? You use the Windows shutdown -r command.",
"How do you copy files? You use Windows File Explorer",
"How do your partition a disk? You use diskmgmt.msc",
"How do you open calculator? You execute calc.exe",
"How you you add new local users, run task scheduler, or view events? You use compmgmt.msc"
],
embedding=embeddings
)

retriever = vectorstore.as_retriever()

#Text to display status to the user
headerDisplay = "Hello"
detailDisplay = "Please ask a question above"

st.title("Gemini assistant & :red[NLP OS I/F R&D]")

#Create Gemini AI object. Apply the Gemini API Key. Set a loose temperature.
model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=apikey,temperature=0.9,
                                  convert_system_message_to_human=True)

#Prompt the user to input their request.
userQuestion = st.text_area("You can ask general questions, questions about Troy University, and in the future interface with your OS! Press **CTRL+Enter** to send your question.")

#Clear the section which displays results from Gemini.
responseTitle = st.empty()
responseTitle.write("")
responseBody = st.empty()
responseBody.write("")

#The prompt template and prompt.
template = """Answer the question based on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

#Functionality to perform the communication with the API and then display the results.
if userQuestion:
   responseTitle.write("Processing")
   responseBody.write("")   
   chain = RunnableMap({
      "context": lambda x: retriever.get_relevant_documents(x["question"]),
      "question": lambda x: x["question"]
   }) | prompt | model      
   output = chain.invoke({"question": userQuestion})
   responseTitle.write("")
   responseBody.write(output.content)
     
   #Add code here if the response is OS related.
   #The output will be written to FTP flat file or
   #cloud based database. The OS will run a client application
   #to retrieve the output, delete it from the file/database,
   #and then execute the command for the user.

   #This is commented out due to file read errors. I will find a way to reimplement.
   ##qa_chain = RetrievalQA.from_chain_type(lcGemini, retriever=vector_index,return_source_documents=True,chain_type_kwargs={"prompt": qa_chain_prompt})
   ##result = qa_chain({"query": userQuestion})
   ##st.write(result["result"])
   ##userQuestion_Prompt = PromptTemplate.from_template("{userQuestion}")
   ##lcChain = LLMChain(llm=lcGemini, prompt = userQuestion_Prompt, verbose=True)
   ##lcResponse = lcChain.run(userQuestion)
   ###responseTitle.write("")
   #responseBody.write(lcResponse)