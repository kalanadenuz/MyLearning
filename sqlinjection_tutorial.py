"""
Beginner's Guide to SQL Injection - Interactive Tutorial
Learn by doing with safe, commented examples
"""

from colorama import init, Fore, Style

init(autoreset=True)

class SQLInjectionTutorial:
    """Interactive SQL injection learning tool"""
    
    def __init__(self):
        self.score = 0
        self.current_level = 1
    
    def banner(self):
        print(f"{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}SQL INJECTION INTERACTIVE TUTORIAL")
        print(f"{Fore.CYAN}{'='*80}\n")
        print(f"{Fore.YELLOW}Learn the fundamentals of SQL injection through examples\n")
    
    # ==================== LEVEL 1: Understanding SQL ====================
    
    def level1_basic_sql(self):
        """Teach basic SQL queries"""
        print(f"\n{Fore.GREEN}📚 LEVEL 1: Understanding SQL Basics\n")
        
        print(f"{Fore.CYAN}SQL (Structured Query Language) is how we talk to databases.\n")
        
        print(f"{Fore.YELLOW}Example 1: Simple SELECT query")
        print(f"{Fore.WHITE}SELECT * FROM users WHERE username='admin';")
        print(f"{Fore.CYAN}↓ This asks the database: 'Give me all data from users table where username is admin'\n")
        
        print(f"{Fore.YELLOW}Example 2: Login check")
        login_query = "SELECT * FROM users WHERE username='admin' AND password='pass123';"
        print(f"{Fore.WHITE}{login_query}")
        print(f"{Fore.CYAN}↓ If this returns a result, login is successful!\n")
        
        print(f"{Fore.GREEN}[?] Quiz: What does 'WHERE' do in SQL?")
        print(f"a) Filters results based on a condition")
        print(f"b) Deletes data")
        print(f"c) Creates a new table")
        
        answer = input(f"\n{Fore.YELLOW}Your answer (a/b/c): {Fore.WHITE}").lower()
        
        if answer == "a":
            print(f"{Fore.GREEN}✓ Correct! WHERE filters results.\n")
            self.score += 10
            return True
        else:
            print(f"{Fore.RED}✗ Wrong. WHERE is used to filter results based on conditions.\n")
            return False
    
    # ==================== LEVEL 2: How SQL Injection Works ====================
    
    def level2_injection_concept(self):
        """Explain the concept of SQL injection"""
        print(f"\n{Fore.GREEN}📚 LEVEL 2: What is SQL Injection?\n")
        
        print(f"{Fore.CYAN}SQL Injection happens when user input is inserted into SQL queries WITHOUT validation.\n")
        
        print(f"{Fore.YELLOW}Normal Login Process:")
        print(f"{Fore.WHITE}User enters: username='john', password='secret'")
        print(f"{Fore.WHITE}Query becomes: SELECT * FROM users WHERE username='john' AND password='secret';")
        print(f"{Fore.GREEN}↓ Database checks if john/secret exists\n")
        
        print(f"{Fore.YELLOW}SQL Injection Attack:")
        print(f"{Fore.RED}User enters: username='admin'--', password='anything'")
        print(f"{Fore.RED}Query becomes: SELECT * FROM users WHERE username='admin'--' AND password='anything';")
        print(f"                                                                    {Fore.YELLOW}↑↑ Everything after -- is a comment!")
        print(f"{Fore.RED}↓ Actual query executed: SELECT * FROM users WHERE username='admin'")
        print(f"{Fore.RED}↓ Password check is BYPASSED!\n")
        
        print(f"{Fore.CYAN}Key concept: The attacker 'broke out' of the string and modified the query logic.\n")
        
        print(f"{Fore.GREEN}[?] Quiz: What does '--' mean in SQL?")
        print(f"a) Subtraction")
        print(f"b) Comment (ignores rest of line)")
        print(f"c) AND operator")
        
        answer = input(f"\n{Fore.YELLOW}Your answer (a/b/c): {Fore.WHITE}").lower()
        
        if answer == "b":
            print(f"{Fore.GREEN}✓ Correct! -- starts a comment in SQL.\n")
            self.score += 10
            return True
        else:
            print(f"{Fore.RED}✗ Wrong. -- is a comment in SQL (like # in Python).\n")
            return False
    
    # ==================== LEVEL 3: Crafting Payloads ====================
    
    def level3_payloads(self):
        """Teach payload construction"""
        print(f"\n{Fore.GREEN}📚 LEVEL 3: Crafting SQL Injection Payloads\n")
        
        print(f"{Fore.CYAN}Let's practice creating injection payloads!\n")
        
        print(f"{Fore.YELLOW}Scenario: Login form with vulnerable query:")
        print(f"{Fore.WHITE}SELECT * FROM users WHERE username='USER_INPUT' AND password='PASSWORD_INPUT';")
        print(f"\n{Fore.CYAN}Your goal: Bypass the login without knowing the password.\n")
        
        print(f"{Fore.YELLOW}Challenge 1: Complete this payload")
        print(f"{Fore.WHITE}Username: admin")
        print(f"{Fore.WHITE}What should you add to username to comment out the password check?")
        print(f"\nHint: You need to close the quote and start a comment\n")
        
        print(f"a) admin'--")
        print(f"b) admin--")
        print(f"c) admin' AND '1'='1")
        
        answer = input(f"\n{Fore.YELLOW}Your answer (a/b/c): {Fore.WHITE}").lower()
        
        if answer == "a":
            print(f"{Fore.GREEN}✓ Correct!\n")
            print(f"{Fore.CYAN}Explanation:")
            print(f"  1. admin' → Closes the username string")
            print(f"  2. --     → Comments out everything after")
            print(f"  3. Final query: SELECT * FROM users WHERE username='admin'--' AND password='...'")
            print(f"                                                               {Fore.YELLOW}[This part is ignored]")
            self.score += 10
            return True
        else:
            print(f"{Fore.RED}✗ Wrong. You need to close the string with ' and then add --\n")
            print(f"{Fore.CYAN}Correct answer: admin'--")
            return False
    
    # ==================== LEVEL 4: Types of SQL Injection ====================
    
    def level4_types(self):
        """Explain different SQLi types"""
        print(f"\n{Fore.GREEN}📚 LEVEL 4: Types of SQL Injection\n")
        
        print(f"{Fore.CYAN}There are several types of SQL injection:\n")
        
        print(f"{Fore.YELLOW}1. Error-Based SQLi")
        print(f"{Fore.WHITE}   Goal: Trigger database errors to learn about structure")
        print(f"{Fore.WHITE}   Payload: admin' AND 1=CONVERT(int, (SELECT @@version))--")
        print(f"{Fore.CYAN}   ↓ Forces database to show its version in error message\n")
        
        print(f"{Fore.YELLOW}2. Union-Based SQLi")
        print(f"{Fore.WHITE}   Goal: Combine your query with existing one to extract data")
        print(f"{Fore.WHITE}   Payload: admin' UNION SELECT username, password FROM users--")
        print(f"{Fore.CYAN}   ↓ Returns additional data from database\n")
        
        print(f"{Fore.YELLOW}3. Boolean-Based Blind SQLi")
        print(f"{Fore.WHITE}   Goal: Ask true/false questions to extract data")
        print(f"{Fore.WHITE}   Payload: admin' AND (SELECT LEN(password) FROM users WHERE id=1)>5--")
        print(f"{Fore.CYAN}   ↓ If page loads normally: password is longer than 5 characters\n")
        
        print(f"{Fore.YELLOW}4. Time-Based Blind SQLi")
        print(f"{Fore.WHITE}   Goal: Use delays to confirm vulnerability")
        print(f"{Fore.WHITE}   Payload: admin' AND SLEEP(5)--")
        print(f"{Fore.CYAN}   ↓ If page takes 5+ seconds: vulnerable!\n")
        
        print(f"{Fore.GREEN}[?] Quiz: Which type would you use if the page doesn't show errors?")
        print(f"a) Error-Based")
        print(f"b) Boolean or Time-Based Blind")
        print(f"c) Union-Based")
        
        answer = input(f"\n{Fore.YELLOW}Your answer (a/b/c): {Fore.WHITE}").lower()
        
        if answer == "b":
            print(f"{Fore.GREEN}✓ Correct! Blind SQLi is used when you can't see errors.\n")
            self.score += 10
            return True
        else:
            print(f"{Fore.RED}✗ Wrong. Use Blind SQLi when no errors are shown.\n")
            return False
    
    # ==================== LEVEL 5: Detection Techniques ====================
    
    def level5_detection(self):
        """Teach detection methods"""
        print(f"\n{Fore.GREEN}📚 LEVEL 5: Detecting SQL Injection Vulnerabilities\n")
        
        print(f"{Fore.CYAN}How to find SQL injection vulnerabilities:\n")
        
        print(f"{Fore.YELLOW}Step 1: Identify Input Points")
        print(f"{Fore.WHITE}   • URL parameters: ?id=123")
        print(f"{Fore.WHITE}   • Form fields: username, password")
        print(f"{Fore.WHITE}   • Cookies, HTTP headers\n")
        
        print(f"{Fore.YELLOW}Step 2: Test with Special Characters")
        print(f"{Fore.WHITE}   Try these in each input:")
        print(f"{Fore.WHITE}   • Single quote: '")
        print(f"{Fore.WHITE}   • Double quote: \"")
        print(f"{Fore.WHITE}   • SQL comment: --")
        print(f"{Fore.WHITE}   • Boolean test: ' OR '1'='1\n")
        
        print(f"{Fore.YELLOW}Step 3: Analyze Response")
        print(f"{Fore.GREEN}   ✓ SQL error message → VULNERABLE!")
        print(f"{Fore.GREEN}   ✓ Different page content → Possibly vulnerable")
        print(f"{Fore.GREEN}   ✓ Time delay (with SLEEP) → Vulnerable")
        print(f"{Fore.RED}   ✗ Same page/error page → Might be protected\n")
        
        print(f"{Fore.CYAN}Practical Example:\n")
        print(f"{Fore.WHITE}URL: http://example.com/product?id=5")
        print(f"{Fore.YELLOW}Test 1: http://example.com/product?id=5'")
        print(f"{Fore.RED}Response: 'SQL syntax error near '5'''")
        print(f"{Fore.GREEN}↓ VULNERABLE! Error reveals SQL is being executed.\n")
        
        print(f"{Fore.GREEN}[?] What's the first thing to test for SQL injection?")
        print(f"a) Complex UNION queries")
        print(f"b) Single quote (') in input")
        print(f"c) Time delays")
        
        answer = input(f"\n{Fore.YELLOW}Your answer (a/b/c): {Fore.WHITE}").lower()
        
        if answer == "b":
            print(f"{Fore.GREEN}✓ Correct! Always start simple with a single quote.\n")
            self.score += 10
            return True
        else:
            print(f"{Fore.RED}✗ Wrong. Start with simple tests like single quote.\n")
            return False
    
    # ==================== LEVEL 6: Prevention ====================
    
    def level6_prevention(self):
        """Teach prevention methods"""
        print(f"\n{Fore.GREEN}📚 LEVEL 6: Preventing SQL Injection\n")
        
        print(f"{Fore.CYAN}How developers should protect against SQL injection:\n")
        
        print(f"{Fore.RED}❌ BAD CODE (Vulnerable):")
        print(f'{Fore.WHITE}username = request.form["username"]')
        print(f'{Fore.WHITE}query = "SELECT * FROM users WHERE username=\'" + username + "\'"')
        print(f'{Fore.RED}↓ User input directly in query = DANGER!\n')
        
        print(f"{Fore.GREEN}✓ GOOD CODE (Safe - Parameterized Query):")
        print(f'{Fore.WHITE}username = request.form["username"]')
        print(f'{Fore.WHITE}query = "SELECT * FROM users WHERE username=?"')
        print(f'{Fore.WHITE}cursor.execute(query, (username,))')
        print(f'{Fore.GREEN}↓ Database treats input as DATA, not CODE!\n')
        
        print(f"{Fore.YELLOW}Other Prevention Methods:")
        print(f"{Fore.WHITE}1. Use ORM (Object-Relational Mapping) libraries")
        print(f"{Fore.WHITE}2. Input validation (whitelist allowed characters)")
        print(f"{Fore.WHITE}3. Least privilege (database user has minimal permissions)")
        print(f"{Fore.WHITE}4. WAF (Web Application Firewall)\n")
        
        print(f"{Fore.GREEN}[?] What's the BEST way to prevent SQL injection?")
        print(f"a) Block single quotes")
        print(f"b) Use parameterized queries")
        print(f"c) Hide error messages")
        
        answer = input(f"\n{Fore.YELLOW}Your answer (a/b/c): {Fore.WHITE}").lower()
        
        if answer == "b":
            print(f"{Fore.GREEN}✓ Correct! Parameterized queries are the gold standard.\n")
            self.score += 10
            return True
        else:
            print(f"{Fore.RED}✗ Wrong. Parameterized queries are the best defense.\n")
            return False
    
    # ==================== Main Tutorial Flow ====================
    
    def run(self):
        """Run the complete tutorial"""
        self.banner()
        
        input(f"{Fore.CYAN}Press Enter to start the tutorial...\n")
        
        # Run all levels
        levels = [
            self.level1_basic_sql,
            self.level2_injection_concept,
            self.level3_payloads,
            self.level4_types,
            self.level5_detection,
            self.level6_prevention
        ]
        
        for level_func in levels:
            level_func()
            input(f"\n{Fore.CYAN}Press Enter to continue to next level...\n")
        
        # Final score
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.GREEN}🎉 TUTORIAL COMPLETE!")
        print(f"{Fore.CYAN}{'='*80}\n")
        
        max_score = 60
        percentage = (self.score / max_score) * 100
        
        print(f"{Fore.YELLOW}Your Score: {self.score}/{max_score} ({percentage:.0f}%)\n")
        
        if percentage >= 80:
            print(f"{Fore.GREEN}⭐⭐⭐ Excellent! You understand SQL injection well.")
        elif percentage >= 60:
            print(f"{Fore.YELLOW}⭐⭐ Good job! Review the topics you missed.")
        else:
            print(f"{Fore.RED}⭐ Keep learning! Go through the tutorial again.")
        
        print(f"\n{Fore.CYAN}Next Steps:")
        print(f"{Fore.WHITE}1. Practice on DVWA (Damn Vulnerable Web App)")
        print(f"{Fore.WHITE}2. Try WebGoat tutorials")
        print(f"{Fore.WHITE}3. Learn to use SQLMap tool")
        print(f"{Fore.WHITE}4. Read OWASP SQL Injection documentation")
        print(f"{Fore.WHITE}5. Join CTF competitions\n")


if __name__ == "__main__":
    tutorial = SQLInjectionTutorial()
    tutorial.run()
