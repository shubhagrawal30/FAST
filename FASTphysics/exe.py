import server
import os, sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", \
                os.path.join(os.getcwd(), "server.py"), \
                "--browser.gatherUsageStats=false"]
    sys.exit(stcli.main())