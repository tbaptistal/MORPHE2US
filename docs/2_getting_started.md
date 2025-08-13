# Getting Started

Welcome! This guide will help you install and launch MORPHE2US for the first time.

---

## System Requirements

There are no strict hardware requirements, but here are some guidelines:

| Component         | Notes                                                                 |
|------------------|-----------------------------------------------------------------------|
| **Operating System** | Any (Windows, macOS, Linux)                                            |
| **Processor**        | Faster CPUs will reduce simulation time                              |
| **RAM**              | Depends on model complexity and scale                                |
| **Python**           | Required for the MORPHE2US pipeline (recommend Python 3.8+)          |
| **SpineToolBox**     | Required (see installation below)                                    |
| **SpineOpt**         | Required (see installation below)                                    |

---

## Installation Steps

### 1. Install Python & dependencies

We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas openpyxl
