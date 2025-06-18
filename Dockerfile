FROM python:3.12.9-slim

# disable print buffering
ENV PYTHONUNBUFFERED=1 \
# don't generate __pycache__
PYTHONDONTWRITEBYTECODE=1 \
# even if we run `python abc/xyz.py`, we want to import from project root, not abc.
PYTHONPATH=.

WORKDIR /usr/src/app
RUN pip install --no-cache-dir 'poetry>=1.5' debugpy

COPY poetry.lock pyproject.toml ./
# We don't copy everything, as we only want to reinstall dependencies if poetry.lock / pyproject.toml change.
# At each step, docker build doesn't use cache if any of the workdir files have changed since last build.

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-root 

COPY . .

# Set the arguments for the username, UID, and GID
ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create a non-root user with the specified username, UID, and GID
RUN groupadd --gid $USER_GID $USERNAME \
&& useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Change the ownership of the working directory to the "appuser"
RUN chown -R $USERNAME:$USERNAME .

# Switch to the "appuser"
USER $USERNAME

# Run FastAPI with reload enabled
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7788"]