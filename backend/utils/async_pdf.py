# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Async PDF generation for better user experience"""

import asyncio
import threading
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from pathlib import Path
import queue
import uuid
from config import OPTIMIZATIONS

class AsyncPDFGenerator:
    """Generate PDFs asynchronously without blocking the main response"""

    def __init__(self):
        self.pdf_queue = queue.Queue()
        self.results = {}
        self.callbacks = {}
        self._start_worker()

    def _start_worker(self):
        """Start background worker thread for PDF generation"""
        worker_thread = threading.Thread(target=self._pdf_worker, daemon=True)
        worker_thread.start()

    def _pdf_worker(self):
        """Worker thread that processes PDF generation requests"""
        while True:
            try:
                # Wait for PDF generation request
                task = self.pdf_queue.get(timeout=1)
                if task is None:
                    break

                task_id = task['id']
                analysis_results = task['analysis_results']
                callback = task.get('callback')

                # Generate PDF
                try:
                    from utils.pdf_generator import PDFGenerator
                    pdf_generator = PDFGenerator()
                    report_data = self._structure_report_data(analysis_results)

                    # Generate PDF
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_dir = Path("generated_reports")
                    output_dir.mkdir(exist_ok=True)

                    output_path = output_dir / f"deal_sourcing_report_{timestamp}.pdf"
                    pdf_path = pdf_generator.generate_pdf(report_data, str(output_path))

                    result = {
                        "success": True,
                        "pdf_path": str(pdf_path),
                        "download_url": f"/download/{output_path.name}",
                        "report_name": output_path.name,
                        "task_id": task_id
                    }
                except Exception as e:
                    result = {
                        "success": False,
                        "error": str(e),
                        "task_id": task_id
                    }

                # Store result
                self.results[task_id] = result

                # Call callback if provided
                if callback:
                    callback(result)

            except queue.Empty:
                continue
            except Exception:
                continue

    def generate_async(
        self,
        analysis_results: str,
        callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Generate PDF asynchronously

        Args:
            analysis_results: The analysis results to convert to PDF
            callback: Optional callback function to call when PDF is ready

        Returns:
            Immediate response with task ID for tracking
        """
        if not OPTIMIZATIONS["async_pdf"]:
            # Fall back to synchronous generation
            from pdf_agent import generate_pdf_report
            return generate_pdf_report(analysis_results)

        # Create task ID
        task_id = str(uuid.uuid4())

        # Queue the task
        task = {
            'id': task_id,
            'analysis_results': analysis_results,
            'callback': callback
        }
        self.pdf_queue.put(task)

        # Return immediate response
        return {
            "success": True,
            "task_id": task_id,
            "status": "processing",
            "message": "PDF generation started in background. Check status with task_id."
        }

    def get_status(self, task_id: str) -> Dict[str, Any]:
        """Check status of PDF generation task"""
        if task_id in self.results:
            return self.results[task_id]
        else:
            return {
                "task_id": task_id,
                "status": "processing",
                "message": "PDF still being generated"
            }

    def _structure_report_data(self, analysis_results: str) -> Dict[str, Any]:
        """Structure the analysis results for PDF generation"""
        # This is a simplified version - reuse from pdf_agent.py
        report_data = {
            'subtitle': 'AI-Powered Investment Opportunity Analysis',
            'executive_summary': {
                'metrics': {'total_opportunities': 0},
                'key_findings': [],
                'recommendations': []
            },
            'opportunities': [],
            'risk_analysis': {
                'overall_risk': 'Medium',
                'market_risks': [],
                'mitigation_strategies': []
            },
            'additional_content': analysis_results
        }

        # Parse analysis results
        lines = analysis_results.split('\n')
        for line in lines[:10]:  # Quick parse for async
            if line.strip():
                if 'opportunity' in line.lower():
                    report_data['executive_summary']['metrics']['total_opportunities'] += 1

        return report_data

# Global async PDF generator instance
_async_pdf_generator = None

def get_async_pdf_generator() -> AsyncPDFGenerator:
    """Get or create the global async PDF generator"""
    global _async_pdf_generator
    if _async_pdf_generator is None:
        _async_pdf_generator = AsyncPDFGenerator()
    return _async_pdf_generator

def generate_pdf_async(analysis_results: str) -> Dict[str, Any]:
    """Generate PDF report asynchronously for immediate response.

    Returns immediately with task ID while PDF generation happens in background.
    """
    generator = get_async_pdf_generator()
    return generator.generate_async(analysis_results)

def check_pdf_status(task_id: str) -> Dict[str, Any]:
    """Check status of async PDF generation task."""
    generator = get_async_pdf_generator()
    return generator.get_status(task_id)