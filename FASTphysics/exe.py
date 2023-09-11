import os, sys, server
import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", \
                os.path.join(os.path.dirname(__file__), "server.py"), \
                "--browser.gatherUsageStats=false"]
    sys.exit(stcli.main())