#!/bin/bash

source ./common.cfg

env_name=$1

ERR_MSG="[ERROR] Please provide valid conda environment name as the first argument."

if [ ! $env_name ] ; then
    echo $ERR_MSG
    exit
fi

# If environment is actually a file path (e.g. "../environments/py2.7/m2-4.5.11/cc-env-r20181008/")
# then just take the last component as the env name.
env_name=$(basename $env_name)

channel_urls_fname="channel-urls.txt"
pip_fname="pip.txt"

spec_file_dir=$(get_env_path $env_name)

spec_file_path=${spec_file_dir}/${channel_urls_fname}
pip_file_path=${spec_file_dir}/${pip_fname}

path_comps=$(echo $spec_file_dir | rev | cut -d/ -f2-3 | rev)

# Run miniconda installer: does nothing if already installed
py_version=$(echo $path_comps | cut -d/ -f1)
./install-miniconda.sh ${py_version}

if [ $? -ne 0 ]; then
    echo "[ERROR] Miniconda install failed so stopping."
    exit
fi

bin_dir=${JASPY_BASE_DIR}/jaspy/miniconda_envs/jas${path_comps}/bin
export PATH=${bin_dir}:$PATH

cmd="${bin_dir}/conda create --name ${env_name} --file ${spec_file_path} -c ${JASPY_CHANNEL_URL}/jas${path_comps} --override-channels --yes"
echo "[INFO] Running: $cmd"
$cmd

echo "[INFO] Created conda environment: $env_name"

if [ -f $pip_file_path ]; then
    echo "[INFO] Installing additional packages via PIP..."
    source ${bin_dir}/activate $env_name
    ${bin_dir}/conda install --yes pip
    pip install --upgrade pip
    pip install -r ${pip_file_path} 
fi

echo "[INFO] You can activate and use this environment with:"
echo "  export PATH=${bin_dir}:\$PATH"
echo "  source activate $env_name"

