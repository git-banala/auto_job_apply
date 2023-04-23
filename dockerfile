FROM python:3

# set the working directory to /app
WORKDIR /app

# install the required packages
RUN pip install selenium

# copy the script into the container
COPY scripts/dice_auto_apply.py /app

# run the script
CMD ["python", "dice_auto_apply.py"]
