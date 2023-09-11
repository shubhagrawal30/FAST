import os, sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        application_path = os.path.join(os.path.dirname(sys.executable))
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    sys.argv = ["streamlit", "run", \
                os.path.join(application_path, "server.py"), \
                "--browser.gatherUsageStats=false", "--server.enableCORS=true",
                "--server.enableXsrfProtection=false"]
    sys.exit(stcli.main())