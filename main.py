from crew import crew

company = input("Enter a company name or ticker: ")
result = crew.kickoff(inputs={"company": company})
print("\n\n### FINAL REPORT ###\n")
print(result)