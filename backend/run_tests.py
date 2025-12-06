from language_detector import detect_language, verify_submission, friendly_name
import test_samples
import sys
import os

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Utility to suppress print output from verify_submission during tests
class SuppressPrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def run_accuracy_tests():
    """
    PHASE 1: Verify that every sample is correctly identified as its own language.
    """
    print(f"\n{YELLOW}--- PHASE 1: ACCURACY (Self-Identity Check) ---{RESET}")
    passed = 0
    failed = 0
    
    for key, code in test_samples.samples.items():
        # logic: "python_complex" -> expected "python"
        expected = key.split("_")[0]
        
        # Run detection
        detected = detect_language(code)
        
        if detected == expected:
            print(f"{GREEN}✔ PASS{RESET} : {key:<25} -> Detected: {detected}")
            passed += 1
        else:
            print(f"{RED}✘ FAIL{RESET} : {key:<25}")
            print(f"    ├── Expected: {expected}")
            print(f"    └── Detected: {detected}")
            failed += 1
            
    return passed, failed

def run_cross_contamination_tests():
    """
    PHASE 2: Verify that every sample is REJECTED when submitted as a different language.
    This dynamically tests every sample against every language.
    """
    print(f"\n{YELLOW}--- PHASE 2: ISOLATION (Cross-Contamination Check) ---{RESET}")
    print("Attempting to submit every code sample as every WRONG language...")
    
    passed = 0
    failed = 0
    total_checks = 0
    
    # Get list of all supported languages from the detector config
    all_supported_langs = list(friendly_name.keys())
    
    # Iterate through EVERY sample in the test file
    for sample_key, code_snippet in test_samples.samples.items():
        real_lang = sample_key.split("_")[0]
        
        # Try to submit this code snippet as every OTHER language
        for fake_label in all_supported_langs:
            # Skip if the fake label is actually the correct one
            if fake_label == real_lang: continue 
            if fake_label == "unknown": continue

            total_checks += 1
            
            # Run verification (suppressing the "Supreme Alert" printouts for cleaner test logs)
            with SuppressPrint():
                is_valid, detected = verify_submission(code_snippet, fake_label)
            
            # SUCCESS criteria: The system must return False (Reject)
            if is_valid is False:
                passed += 1
            else:
                # FAILURE: The system accepted mismatched code
                print(f"{RED}✘ BREACH{RESET} : Submitted {sample_key} ({real_lang}) as {fake_label} -> ACCEPTED!")
                failed += 1

    print(f"Total Isolation Scenarios Tested: {total_checks}")
    return passed, failed

if __name__ == "__main__":
    print("==================================================")
    print("       SUPREME ANALYST DIAGNOSTICS v5.0")
    print("==================================================")

    acc_pass, acc_fail = run_accuracy_tests()
    sec_pass, sec_fail = run_cross_contamination_tests()

    print("\n==================================================")
    print(f"Accuracy  : {acc_pass} passed, {acc_fail} failed")
    print(f"Isolation : {sec_pass} passed, {sec_fail} failed")
    print("==================================================")
    
    if acc_fail == 0 and sec_fail == 0:
        print(f"{GREEN}🎉 SYSTEM SECURE. All languages detected and isolated correctly.{RESET}")
    else:
        print(f"{RED}⚠ SYSTEM COMPROMISED. Review failures above.{RESET}")