# import requests
# import json
# import time
# import os
# from typing import Dict, Any

# class OllamaAgent:
#     def __init__(self, base_url: str = "http://ollama:11434"):
#         self.base_url = base_url
#         self.model = "neural-chat"
        
#     def generate_response(self, prompt: str) -> Dict[Any, Any]:
#         url = f"{self.base_url}/api/generate"
        
#         payload = {
#             "model": self.model,
#             "prompt": prompt,
#             "stream": False
#         }
        
#         try:
#             response = requests.post(url, json=payload)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             print(f"Erreur lors de la requête: {e}")
#             return {"error": str(e)}

#     def chat(self, message: str) -> str:
#         response = self.generate_response(message)
#         return response.get("response", "Désolé, je n'ai pas pu générer de réponse.")

# def main():
#     agent = OllamaAgent()
    
#     # Exemple de conversation
#     questions = [
#         "Bonjour, qui es-tu?",
#         "Que peux-tu faire?",
#         "Explique-moi un concept d'IA en termes simples."
#     ]
    
#     for question in questions:
#         print(f"\nQuestion: {question}")
#         print("Réponse:", agent.chat(question))
#         time.sleep(1)  # Petit délai entre les questions

# if __name__ == "__main__":
#     # Attendre que le service Ollama soit prêt
#     time.sleep(10)
#     main()

##########################################################################

# import requests
# import json
# import time
# import os
# from typing import Dict, Any
# from colorama import init, Fore, Style
# import signal
# import sys

# init(autoreset=True)  # Initialise colorama

# class OllamaAgent:
#     def __init__(self, base_url: str = "http://ollama:11434"):
#         self.base_url = base_url
#         self.model = "neural-chat"
#         self.conversation_history = []
        
#     def generate_response(self, prompt: str) -> Dict[Any, Any]:
#         url = f"{self.base_url}/api/generate"
        
#         context = "\n".join(self.conversation_history[-5:])  # Garde les 5 dernières interactions
#         full_prompt = f"{context}\n{prompt}" if context else prompt
        
#         payload = {
#             "model": self.model,
#             "prompt": full_prompt,
#             "stream": False,
#             "context": self.get_context()
#         }
        
#         try:
#             response = requests.post(url, json=payload)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             print(f"{Fore.RED}Erreur lors de la requête: {e}{Style.RESET_ALL}")
#             return {"error": str(e)}

#     def get_context(self):
#         url = f"{self.base_url}/api/show"
#         try:
#             response = requests.post(url, json={"model": self.model})
#             if response.status_code == 200:
#                 return response.json().get("context", [])
#         except:
#             return []

#     def chat(self, message: str) -> str:
#         if message.strip().lower() in ['exit', 'quit', 'bye']:
#             print(f"\n{Fore.YELLOW}Au revoir! 👋{Style.RESET_ALL}")
#             sys.exit(0)
            
#         response = self.generate_response(message)
#         response_text = response.get("response", "Désolé, je n'ai pas pu générer de réponse.")
        
#         # Mise à jour de l'historique
#         self.conversation_history.append(f"User: {message}")
#         self.conversation_history.append(f"Assistant: {response_text}")
        
#         return response_text

# def signal_handler(sig, frame):
#     print(f"\n{Fore.YELLOW}Au revoir! 👋{Style.RESET_ALL}")
#     sys.exit(0)

# def print_welcome():
#     welcome_message = f"""
# {Fore.CYAN}╔══════════════════════════════════════════╗
# ║     Assistant IA - Interface de Chat      ║
# ╚══════════════════════════════════════════╝{Style.RESET_ALL}

# {Fore.GREEN}Instructions:{Style.RESET_ALL}
# - Tapez votre message et appuyez sur Entrée
# - Tapez 'exit', 'quit' ou 'bye' pour quitter
# - Utilisez Ctrl+C pour quitter à tout moment

# {Fore.YELLOW}Chat démarré... Posez votre question !{Style.RESET_ALL}
# """
#     print(welcome_message)

# def main():
#     # Gestion du Ctrl+C
#     signal.signal(signal.SIGINT, signal_handler)
    
#     # Attendre que le service Ollama soit prêt
#     print(f"{Fore.YELLOW}Connexion à Ollama...{Style.RESET_ALL}")
#     time.sleep(5)
    
#     agent = OllamaAgent()
#     print_welcome()
    
#     while True:
#         try:
#             user_input = input(f"{Fore.GREEN}Vous ➜ {Style.RESET_ALL}")
#             if not user_input.strip():
#                 continue
                
#             print(f"{Fore.BLUE}Assistant ➜ {Style.RESET_ALL}", end='')
#             response = agent.chat(user_input)
#             print(response)
#             print()  # Ligne vide pour la lisibilité
            
#         except Exception as e:
#             print(f"\n{Fore.RED}Une erreur est survenue: {e}{Style.RESET_ALL}")

# if __name__ == "__main__":
#     main()

####################################################################################
# import requests
# import json
# import time
# import os
# from typing import Dict, Any
# from colorama import init, Fore, Style
# import signal
# import sys
# import uuid
# from memory_manager import MemoryManager
# from datetime import datetime

# init(autoreset=True)

# class OllamaAgent:
#     def __init__(self, base_url: str = "http://ollama:11434"):
#         self.base_url = base_url
#         self.model = "neural-chat"
#         self.memory_manager = MemoryManager()
#         self.current_conversation_id = str(uuid.uuid4())
        
#     def generate_response(self, prompt: str, include_memory: bool = True) -> Dict[Any, Any]:
#         url = f"{self.base_url}/api/generate"
        
#         # Construire le contexte avec la mémoire
#         context = self._build_context(prompt) if include_memory else ""
#         full_prompt = f"{context}\n\nActuelle question: {prompt}"
        
#         payload = {
#             "model": self.model,
#             "prompt": full_prompt,
#             "stream": False
#         }
        
#         try:
#             response = requests.post(url, json=payload)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             print(f"{Fore.RED}Erreur lors de la requête: {e}{Style.RESET_ALL}")
#             return {"error": str(e)}

#     def _build_context(self, prompt: str) -> str:
#         # Récupérer les souvenirs pertinents
#         relevant_memories = self.memory_manager.get_relevant_memories(prompt)
#         recent_context = self.memory_manager.get_conversation_context(
#             self.current_conversation_id
#         )
        
#         context_parts = []
        
#         if relevant_memories:
#             context_parts.append("Souvenirs pertinents:")
#             for memory in relevant_memories:
#                 context_parts.append(
#                     f"[{memory['timestamp']}] {memory['role']}: {memory['content']}"
#                 )
        
#         if recent_context:
#             context_parts.append("\nConversation actuelle:")
#             for msg in reversed(recent_context):
#                 context_parts.append(f"{msg['role']}: {msg['content']}")
        
#         return "\n".join(context_parts)

#     def chat(self, message: str) -> str:
#         if message.startswith("/"):
#             return self._handle_command(message)
            
#         # Sauvegarder le message utilisateur
#         self.memory_manager.add_memory(
#             "user",
#             message,
#             self.current_conversation_id,
#             {"timestamp": datetime.now().isoformat()}
#         )
        
#         response = self.generate_response(message)
#         response_text = response.get("response", "Désolé, je n'ai pas pu générer de réponse.")
        
#         # Sauvegarder la réponse
#         self.memory_manager.add_memory(
#             "assistant",
#             response_text,
#             self.current_conversation_id,
#             {"timestamp": datetime.now().isoformat()}
#         )
        
#         return response_text

#     def _handle_command(self, command: str) -> str:
#         parts = command.split()
#         cmd = parts[0].lower()
        
#         if cmd == "/new":
#             self.current_conversation_id = str(uuid.uuid4())
#             return "Nouvelle conversation démarrée."
            
#         elif cmd == "/context":
#             context = self.memory_manager.get_conversation_context(
#                 self.current_conversation_id
#             )
#             return "\n".join([
#                 f"{msg['role']}: {msg['content']}" for msg in reversed(context)
#             ])
            
#         elif cmd == "/memory":
#             if len(parts) > 1:
#                 query = " ".join(parts[1:])
#                 memories = self.memory_manager.get_relevant_memories(query)
#                 return "\n".join([
#                     f"[{mem['timestamp']}] {mem['role']}: {mem['content']}" 
#                     for mem in memories
#                 ])
#             return "Usage: /memory <query>"
            
#         return f"Commande inconnue: {cmd}"

# def signal_handler(sig, frame):
#     print(f"\n{Fore.YELLOW}Au revoir! 👋{Style.RESET_ALL}")
#     sys.exit(0)

# def print_welcome():
#     welcome_message = f"""
# {Fore.CYAN}╔══════════════════════════════════════════╗
# ║     Assistant IA - Interface de Chat      ║
# ╚══════════════════════════════════════════╝{Style.RESET_ALL}

# {Fore.GREEN}Commandes disponibles:{Style.RESET_ALL}
# /new    - Démarrer une nouvelle conversation
# /context - Voir le contexte de la conversation actuelle
# /memory <query> - Rechercher dans les souvenirs
# exit, quit, bye - Quitter

# {Fore.YELLOW}Chat démarré... Posez votre question !{Style.RESET_ALL}
# """
#     print(welcome_message)

# def main():
#     signal.signal(signal.SIGINT, signal_handler)
#     print(f"{Fore.YELLOW}Connexion à Ollama...{Style.RESET_ALL}")
#     time.sleep(5)
    
#     agent = OllamaAgent()
#     print_welcome()
    
#     while True:
#         try:
#             user_input = input(f"{Fore.GREEN}Vous ➜ {Style.RESET_ALL}")
#             if not user_input.strip():
#                 continue
                
#             if user_input.lower() in ['exit', 'quit', 'bye']:
#                 print(f"\n{Fore.YELLOW}Au revoir! 👋{Style.RESET_ALL}")
#                 break
                
#             print(f"{Fore.BLUE}Assistant ➜ {Style.RESET_ALL}", end='')
#             response = agent.chat(user_input)
#             print(response)
#             print()
            
#         except Exception as e:
#             print(f"\n{Fore.RED}Une erreur est survenue: {e}{Style.RESET_ALL}")

# if __name__ == "__main__":
#     main()

####################################################################################

import requests
import json
import time
import os
import sys
from typing import Dict, Any
from colorama import init, Fore, Style
import signal
import uuid
from memory_manager import MemoryManager
from datetime import datetime

init(autoreset=True)

class OllamaAgent:
    def __init__(self, base_url: str = "http://ollama:11434"):
        self.base_url = base_url
        self.model = "neural-chat"
        self.memory_manager = MemoryManager()
        self.current_conversation_id = str(uuid.uuid4())

    def generate_response(self, prompt: str, include_memory: bool = True) -> Dict[Any, Any]:
        url = f"{self.base_url}/api/generate"
        
        context = self._build_context(prompt) if include_memory else ""
        full_prompt = f"{context}\n\nActuelle question: {prompt}"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": True
        }
        
        try:
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        chunk = json_response['response']
                        print(chunk, end='', flush=True)
                        full_response += chunk
            print()
            return {"response": full_response}
        
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Erreur lors de la requête: {e}{Style.RESET_ALL}")
            return {"error": str(e)}

    def _build_context(self, prompt: str) -> str:
        relevant_memories = self.memory_manager.get_relevant_memories(prompt)
        recent_context = self.memory_manager.get_conversation_context(
            self.current_conversation_id
        )
        
        context_parts = []
        
        if relevant_memories:
            context_parts.append("Souvenirs pertinents:")
            for memory in relevant_memories:
                context_parts.append(
                    f"[{memory['timestamp']}] {memory['role']}: {memory['content']}"
                )
        
        if recent_context:
            context_parts.append("\nConversation actuelle:")
            for msg in reversed(recent_context):
                context_parts.append(f"{msg['role']}: {msg['content']}")
        
        return "\n".join(context_parts)

    def chat(self, message: str) -> str:
        if message.startswith("/"):
            return self._handle_command(message)
            
        self.memory_manager.add_memory(
            "user",
            message,
            self.current_conversation_id,
            {"timestamp": datetime.now().isoformat()}
        )
        
        print(f"{Fore.BLUE}Assistant ➜ {Style.RESET_ALL}", end='', flush=True)
        response = self.generate_response(message)
        response_text = response.get("response", "Désolé, je n'ai pas pu générer de réponse.")
        
        self.memory_manager.add_memory(
            "assistant",
            response_text,
            self.current_conversation_id,
            {"timestamp": datetime.now().isoformat()}
        )
        
        return response_text

    def _handle_command(self, command: str) -> str:
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == "/new":
            self.current_conversation_id = str(uuid.uuid4())
            return "Nouvelle conversation démarrée."
            
        elif cmd == "/context":
            context = self.memory_manager.get_conversation_context(
                self.current_conversation_id
            )
            return "\n".join([
                f"{msg['role']}: {msg['content']}" for msg in reversed(context)
            ])
            
        elif cmd == "/memory":
            if len(parts) > 1:
                query = " ".join(parts[1:])
                memories = self.memory_manager.get_relevant_memories(query)
                return "\n".join([
                    f"[{mem['timestamp']}] {mem['role']}: {mem['content']}" 
                    for mem in memories
                ])
            return "Usage: /memory <query>"
            
        return f"Commande inconnue: {cmd}"

def signal_handler(sig, frame):
    print(f"\n{Fore.YELLOW}Au revoir! 👋{Style.RESET_ALL}")
    sys.exit(0)

def print_welcome():
    welcome_message = f"""
{Fore.CYAN}╔══════════════════════════════════════════╗
║     Assistant IA - Interface de Chat      ║
╚══════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}Commandes disponibles:{Style.RESET_ALL}
/new    - Démarrer une nouvelle conversation
/context - Voir le contexte de la conversation actuelle
/memory <query> - Rechercher dans les souvenirs
exit, quit, bye - Quitter

{Fore.YELLOW}Chat démarré... Posez votre question !{Style.RESET_ALL}
"""
    print(welcome_message)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print(f"{Fore.YELLOW}Connexion à Ollama...{Style.RESET_ALL}")
    time.sleep(5)
    
    agent = OllamaAgent()
    print_welcome()
    
    while True:
        try:
            user_input = input(f"{Fore.GREEN}Vous ➜ {Style.RESET_ALL}")
            if not user_input.strip():
                continue
                
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"\n{Fore.YELLOW}Au revoir! 👋{Style.RESET_ALL}")
                break
                
            response = agent.chat(user_input)
            print()
            
        except Exception as e:
            print(f"\n{Fore.RED}Une erreur est survenue: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()