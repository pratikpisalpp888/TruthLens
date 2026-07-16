# 🔍 TruthLens: AI-Powered Financial Fraud Detection

![TruthLens Dashboard](https://img.shields.io/badge/Status-Live-success?style=for-the-badge) ![Tech Stack](https://img.shields.io/badge/Stack-Next.js%20|%20FastAPI%20|%20Llama%203-blue?style=for-the-badge)

**TruthLens** is an enterprise-grade, multi-agent AI system designed specifically for Indian financial institutions to detect loan and document fraud. By combining deep mathematical analysis, image forensics, and Corrective RAG (CRAG), TruthLens moves beyond simple OCR to mathematically and visually verify the authenticity of financial applications.

---

## 🚀 The Core Innovations

We built TruthLens to think like a seasoned bank fraud investigator. Here are the major innovations that set our pipeline apart:

### 1. Mathematical Fraud Detection (Benford's Law)
Humans are terrible at faking random numbers. When fraudsters fabricate Bank Statements or ITRs, they naturally use round numbers or unnatural digit distributions.
* **The Logic:** TruthLens runs extracted financial data through **Benford's Law** (the mathematical law of anomalous numbers) and **Numeric Entropy Analysis**. If the numbers deviate from natural financial distributions, the AI mathematically proves the document is fabricated.

### 2. Corrective RAG (CRAG) for Regulatory Compliance
* **The Logic:** Hallucinations are unacceptable in finance. When our AI flags an anomaly, it doesn't just guess what the penalty is. It uses **Corrective RAG (CRAG)** connected to a Qdrant vector database to instantly retrieve the exact **RBI regulations and KYC banking guidelines**, grounding its decision in actual law and providing specific regulatory citations.

### 3. GraphRAG (Fraud Network Discovery)
* **The Logic:** Fraudsters rarely work alone. TruthLens uses **GraphRAG (Graph Retrieval-Augmented Generation)** to connect the dots across historical cases. By mapping relationships between IP addresses, PANs, shared devices, and Forged CA Stamps, the AI instantly detects if an applicant is part of a larger organized fraud ring.

### 4. Visual Fraud Annotations (X-Ray Vision)
* **The Logic:** Telling a loan officer "there is fraud" isn't enough; they need proof. TruthLens includes a **Visual Annotation Viewer** that overlays colored bounding boxes directly onto the original PDF. Officers can instantly see exactly where the mathematical anomalies, missing fields, or digital forgeries are located on the page.

### 5. Pixel-Level Forgery Detection (ELA)
* **The Logic:** Using Error Level Analysis (ELA) and compression artifact detection, TruthLens can "see" what the human eye cannot. It detects if a document has been photoshopped, digitally tampered with, or spliced together from multiple sources.

### 6. Military-Grade Data Privacy (Encryption & Local LLMs)
* **The Logic:** Banks cannot send highly sensitive applicant data (Aadhaar, PAN, Bank records) to public APIs like ChatGPT. 
    1. **Encryption at Rest:** All uploaded documents are automatically encrypted on disk using AES encryption and only decrypted in memory.
    2. **Local Llama 3 AI:** TruthLens is powered entirely by a **locally-hosted Llama 3 model (via Ollama)**, ensuring zero PII ever leaves the bank's internal servers.

---

## 🎯 System Architecture: The 5-Agent Pipeline

Instead of relying on a single AI model, TruthLens orchestrates a specialized pipeline of 5 autonomous agents communicating in real-time:

1. **Classifier Agent:** Instantly categorizes uploaded documents (ITR, Bank Statement, PAN) using keyword heuristics.
2. **Forensic Agent:** Runs mathematical (Benford's Law) and pixel-level (Error Level Analysis) checks.
3. **CrossRef Agent:** Cross-references extracted data points across *different* documents (e.g., Does the PAN on the tax return match the Bank Statement name?).
4. **Compliance Agent:** Validates findings against regulatory guidelines using CRAG.
5. **Decision Agent:** Computes a final composite risk score (0-100) and issues a definitive verdict (APPROVE / FLAG / REJECT).

---

## ⚡ Key Features

* **Real-Time Neural Stream:** The frontend uses WebSockets to stream the exact "thoughts" and logs of the AI agents in real-time as they analyze the document.
* **AI Interrogator Chat:** A built-in chat interface where loan officers can "interrogate" the AI about why a specific decision was made, what laws apply, or ask it to explain the forensic findings in simple terms.
* **Instant Extraction:** Uses PyMuPDF as a lightning-fast fallback to instantly read digital PDFs without waiting for slow, traditional visual OCR.

---

## 💻 Tech Stack

* **Frontend:** Next.js (React), TailwindCSS, Framer Motion (for dynamic, premium animations)
* **Backend:** FastAPI (Python), WebSockets
* **AI & NLP:** Llama 3 (via Ollama), LangGraph principles, PyMuPDF
* **Knowledge Base:** Qdrant (Vector Database)
* **Storage:** Local encrypted file storage (MinIO compatible)

---
*Built to bring truth, speed, and mathematical certainty to financial underwriting.*
