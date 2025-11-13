#!/usr/bin/env bash
# Local workspace environment bootstrap for UR workspace
# Sourced conditionally from ~/.bashrc when opening terminals inside the workspace.
# Provides: virtualenv activation, colcon overlay sourcing. (Does not override ROS_DOMAIN_ID.)

WORKSPACE_ROOT="/home/ehayoung/workspaces/ur_workspace"

# Activate Python virtual environment if present
if [ -f "$WORKSPACE_ROOT/.venv/bin/activate" ]; then
  . "$WORKSPACE_ROOT/.venv/bin/activate"
fi

# Source colcon overlay if built and ensure COLCON_CURRENT_PREFIX populated
INSTALL_DIR="$WORKSPACE_ROOT/install"
if [ -f "$INSTALL_DIR/setup.bash" ]; then
  . "$INSTALL_DIR/setup.bash"
  # Fallback: some setups may not export COLCON_CURRENT_PREFIX (older shells or custom build). Set if empty.
  if [ -z "$COLCON_CURRENT_PREFIX" ]; then
    export COLCON_CURRENT_PREFIX="$INSTALL_DIR"
  fi
fi

# (ROS_DOMAIN_ID left unchanged; user global ~/.bashrc sets it.)

# Prevent re-sourcing in same shell
export UR_WORKSPACE_ENV_INITIALIZED=1

# Optional debug banner: enable by exporting UR_WS_DEBUG=1 before sourcing
if [ -n "$UR_WS_DEBUG" ]; then
  echo "[ur_ws] venv=$(command -v python3 2>/dev/null | sed 's|.*/\.venv/.*|active|;t;s|.*|none|') overlay=$COLCON_CURRENT_PREFIX"
fi
