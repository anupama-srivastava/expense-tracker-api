import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import cv2
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils import timezone

from .models import VoiceCommand, OCRReceipt, VoiceAssistantSession
from apps.expenses.models import Expense, Category
from apps.ai.services import AIChatService

logger = logging.getLogger(__name__)


class VoiceCommandService:
    """Service for processing voice commands and natural language expense entry"""
    
    def __init__(self, user):
        self.user = user
        self.ai_service = AIChatService(user)
    
    def process_voice_command(self, audio_file=None, command_text=None) -> Dict[str, Any]:
        """Process voice command and extract expense data"""
        try:
            if not command_text:
                # In production, integrate with speech-to-text service
                command_text = self._mock_speech_to_text(audio_file)
            
            # Process the command text
            processed_data = self._parse_command_text(command_text)
            
            # Create voice command record
            voice_command = VoiceCommand.objects.create(
                user=self.user,
                command_text=command_text,
                transcription=command_text,
                intent=processed_data.get('intent', 'unknown'),
                confidence=processed_data.get('confidence', 0.8),
                is_processed=True
            )
            
            # If it's an expense command, create the expense
            if processed_data.get('intent') == 'add_expense':
                expense = self._create_expense_from_command(processed_data)
                return {
                    'success': True,
                    'message': f'Expense added successfully: {expense.title} - ${expense.amount}',
                    'expense_id': expense.id,
                    'voice_command_id': voice_command.id
                }
            
            return {
                'success': True,
                'message': 'Command processed successfully',
                'data': processed_data,
                'voice_command_id': voice_command.id
            }
            
        except Exception as e:
            logger.error(f"Error processing voice command: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _mock_speech_to_text(self, audio_file) -> str:
        """Mock speech-to-text service (replace with actual service)"""
        # In production, integrate with Google Speech-to-Text, AWS Transcribe, etc.
        return "Add expense for lunch at restaurant for twenty five dollars"
    
    def _parse_command_text(self, text: str) -> Dict[str, Any]:
        """Parse command text to extract intent and data"""
        text_lower = text.lower().strip()
        
        # Intent detection
        if any(word in text_lower for word in ['add', 'create', 'new']):
            return self._parse_add_expense_command(text)
        elif any(word in text_lower for word in ['show', 'list', 'view']):
            return self._parse_show_command(text)
        elif any(word in text_lower for word in ['budget', 'limit']):
            return self._parse_budget_command(text)
        else:
            return {
                'intent': 'query',
                'message': text,
                'confidence': 0.7
            }
    
    def _parse_add_expense_command(self, text: str) -> Dict[str, Any]:
        """Parse add expense command"""
        # Extract amount
        amount = self._extract_amount(text)
        
        # Extract category
        category = self._extract_category(text)
        
        # Extract description
        description = self._extract_description(text)
        
        # Extract merchant
        merchant = self._extract_merchant(text)
        
        return {
            'intent': 'add_expense',
            'amount': amount,
            'category': category,
            'description': description,
            'merchant': merchant,
            'confidence': 0.9
        }
    
    def _parse_show_command(self, text: str) -> Dict[str, Any]:
        """Parse show command"""
        return {
            'intent': 'show_expenses',
            'filters': self._extract_filters(text),
            'confidence': 0.8
        }
    
    def _parse_budget_command(self, text: str) -> Dict[str, Any]:
        """Parse budget command"""
        return {
            'intent': 'budget_info',
            'category': self._extract_category(text),
            'confidence': 0.8
        }
    
    def _extract_amount(self, text: str) -> float:
        """Extract amount from text"""
        import re
        
        # Look for dollar amounts
        dollar_pattern = r'\$(\d+(?:\.\d{2})?)|(\d+(?:\.\d{2})?)\s*dollars?'
        matches = re.findall(dollar_pattern, text, re.IGNORECASE)
        
        if matches:
            amount_str = matches[0][0] if matches[0][0] else matches[0][1]
            return float(amount_str)
        
        # Look for written numbers
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
            'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
            'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
            'eighty': 80, 'ninety': 90, 'hundred': 100
        }
        
        words = text.lower().split()
        for word in words:
            if word in number_words:
                return float(number_words[word])
        
        return 0.0
    
    def _extract_category(self, text: str) -> str:
        """Extract category from text"""
        categories = {
            'food': ['lunch', 'dinner', 'breakfast', 'restaurant', 'cafe', 'food', 'meal'],
            'transport': ['gas', 'uber', 'taxi', 'bus', 'train', 'transport', 'travel'],
            'shopping': ['amazon', 'store', 'shopping', 'clothes', 'electronics'],
            'entertainment': ['movie', 'concert', 'entertainment', 'fun', 'leisure'],
            'utilities': ['electricity', 'water', 'internet', 'phone', 'utilities'],
            'health': ['doctor', 'pharmacy', 'medicine', 'health', 'medical']
        }
        
        text_lower = text.lower()
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'other'
    
    def _extract_description(self, text: str) -> str:
        """Extract description from text"""
        # Remove common phrases
        phrases_to_remove = ['add expense', 'create expense', 'new expense', 'for']
        description = text
        
        for phrase in phrases_to_remove:
            description = description.replace(phrase, '')
        
        return description.strip()
    
    def _extract_merchant(self, text: str) -> str:
        """Extract merchant from text"""
        # Look for proper nouns or known merchants
        words = text.split()
        for word in words:
            if word[0].isupper() and len(word) > 3:
                return word
        
        return ''
    
    def _create_expense_from_command(self, data: Dict[str, Any]) -> Expense:
        """Create expense from parsed command data"""
        category, created = Category.objects.get_or_create(
            name=data['category'],
            defaults={'color': '#3498db'}
        )
        
        expense = Expense.objects.create(
            user=self.user,
            title=data.get('description', 'Voice expense'),
            amount=data['amount'],
            category=category,
            merchant=data.get('merchant', ''),
            transaction_date=timezone.now().date(),
            notes=f"Added via voice command: {data.get('description', '')}"
        )
        
        return expense
    
    def _extract_filters(self, text: str) -> Dict[str, Any]:
        """Extract filters from text"""
        filters = {}
        
        # Time filters
        if 'today' in text.lower():
            filters['date'] = timezone.now().date()
        elif 'this week' in text.lower():
            filters['date_range'] = 'week'
        elif 'this month' in text.lower():
            filters['date_range'] = 'month'
        
        # Category filters
        category = self._extract_category(text)
        if category != 'other':
            filters['category'] = category
        
        return filters


class OCRService:
    """Service for processing receipt images with OCR"""
    
    def __init__(self, user):
        self.user = user
    
    def process_receipt_image(self, image_file) -> Dict[str, Any]:
        """Process receipt image and extract data"""
        try:
            # Save the image
            image_path = default_storage.save(
                f'receipts/{datetime.now().strftime("%Y%m%d_%H%M%S")}_{image_file.name}',
                image_file
            )
            
            # Process the image
            extracted_data = self._extract_receipt_data(image_path)
            
            # Create OCR receipt record
            ocr_receipt = OCRReceipt.objects.create(
                user=self.user,
                image=image_path,
                extracted_data=extracted_data,
                confidence_score=extracted_data.get('confidence', 0.8),
                is_processed=True
            )
            
            # Create expense from extracted data
            if extracted_data.get('amount') and extracted_data.get('merchant'):
                expense = self._create_expense_from_ocr(extracted_data)
                return {
                    'success': True,
                    'message': 'Receipt processed successfully',
                    'expense_id': expense.id,
                    'ocr_receipt_id': ocr_receipt.id,
                    'extracted_data': extracted_data
                }
            
            return {
                'success': True,
                'message': 'Receipt processed but data incomplete',
                'ocr_receipt_id': ocr_receipt.id,
                'extracted_data': extracted_data
            }
            
        except Exception as e:
            logger.error(f"Error processing receipt: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_receipt_data(self, image_path: str) -> Dict[str, Any]:
        """Extract data from receipt image using OCR"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Preprocess image
            processed_image = self._preprocess_image(image)
            
            # Extract text using OCR
            text = pytesseract.image_to_string(processed_image)
            
            # Parse extracted text
            data = self._parse_receipt_text(text)
            
            return data
            
        except Exception as e:
            logger.error(f"Error extracting receipt data: {str(e)}")
            return {
                'error': str(e),
                'confidence': 0.0
            }
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        gray_image = image.convert('L')
        
        # Resize image if too small
        width, height = gray_image.size
        if width < 800:
            new_width = 800
            new_height = int(height * (800 / width))
            gray_image = gray_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply threshold to get better contrast
        import numpy as np
        img_array = np.array(gray_image)
        _, thresholded = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return Image.fromarray(thresholded)
    
    def _parse_receipt_text(self, text: str) -> Dict[str, Any]:
        """Parse extracted text to find relevant data"""
        lines = text.split('\n')
        
        data = {
            'merchant': '',
            'amount': 0.0,
            'date': None,
            'items': [],
            'confidence': 0.8
        }
        
        # Extract merchant (usually first few lines)
        for line in lines[:3]:
            line = line.strip()
            if line and len(line) > 3 and not line.startswith('$'):
                data['merchant'] = line
                break
        
        # Extract amount
        import re
        amount_pattern = r'\$?\d+\.\d{2}'
        amounts = re.findall(amount_pattern, text)
        
        if amounts:
            # Find the largest amount (likely total)
            amounts_float = [float(amount.replace('$', '')) for amount in amounts]
            data['amount'] = max(amounts_float)
        
        # Extract date
        date_pattern = r'\d{1,2}/\d{1,2}/\d{2,4}'
        date_match = re.search(date_pattern, text)
        if date_match:
            try:
                data['date'] = datetime.strptime(date_match.group(), '%m/%d/%Y').date()
            except:
                pass
        
        # Extract items (lines with amounts)
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['item', 'product', 'service']):
                item_amount = re.findall(amount_pattern, line)
                if item_amount:
                    data['items'].append({
                        'description': line,
                        'amount': float(item_amount[0].replace('$', ''))
                    })
        
        return data
    
    def _create_expense_from_ocr(self, data: Dict[str, Any]) -> Expense:
        """Create expense from OCR extracted data"""
        category_name = 'Shopping'  # Default category
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'color': '#e74c3c'}
        )
        
        expense = Expense.objects.create(
            user=self.user,
            title=f"Receipt from {data.get('merchant', 'Unknown')}",
            amount=data['amount'],
            category=category,
            merchant=data.get('merchant', ''),
            transaction_date=data.get('date') or timezone.now().date(),
            notes=f"Processed via OCR: {data.get('items', [])}"
        )
        
        return expense


class VoiceAssistantService:
    """Service for managing voice assistant sessions"""
    
    def __init__(self, user):
        self.user = user
    
    def create_session(self, context: Dict[str, Any] = None) -> VoiceAssistantSession:
        """Create a new voice assistant session"""
        session = VoiceAssistantSession.objects.create(
            user=self.user,
            session_id=f"session_{int(timezone.now().timestamp())}",
            context=context or {}
        )
        return session
    
    def process_session_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """Process a message within a session"""
        try:
            session = VoiceAssistantSession.objects.get(
                user=self.user,
                session_id=session_id,
                is_active=True
            )
            
            # Process message using AI service
            ai_service = AIChatService(self.user)
            response = ai_service.process_message(message, session.context)
            
            # Update session context
            session.context['last_message'] = message
            session.context['last_response'] = response
            session.save()
            
            return response
            
        except VoiceAssistantSession.DoesNotExist:
            return {
                'error': 'Session not found or inactive'
            }
    
    def end_session(self, session_id: str) -> bool:
        """End a voice assistant session"""
        try:
            session = VoiceAssistantSession.objects.get(
                user=self.user,
                session_id=session_id,
                is_active=True
            )
            session.is_active = False
            session.end_time = timezone.now()
            session.save()
            return True
        except VoiceAssistantSession.DoesNotExist:
            return False
