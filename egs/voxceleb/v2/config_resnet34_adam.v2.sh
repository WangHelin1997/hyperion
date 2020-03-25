#Default configuration parameters for the experiment

#xvector training 

#xvector training 
nnet_data=voxceleb2cat_combined
nnet_type=resnet34
batch_size_1gpu=32
eff_batch_size=512 # effective batch size
min_chunk=400
max_chunk=400
ipe=1
lr=0.05
dropout=0
embed_dim=256
s=30
margin_warmup=20
margin=0.3
resnet_opt="--in-channels 1 --in-kernel-size 3 --in-stride 1 --no-maxpool --zero-init-residual"
opt_opt="--opt-optimizer adam --opt-lr $lr --opt-beta1 0.9 --opt-beta2 0.95 --opt-weight-decay 1e-5 --opt-amsgrad"
lrs_opt="--lrsch-lrsch-type exp_lr --lrsch-decay-rate 0.5 --lrsch-decay-steps 8000 --lrsch-hold-steps 40000 --lrsch-min-lr 1e-5 --lrsch-warmup-steps 1000 --lrsch-update-lr-on-opt-step"
nnet_name=resnet34_zir_e${embed_dim}_arc${margin}_do${dropout}_adam_lr${lr}_b${eff_batch_size}.v2
nnet_num_epochs=200
num_augs=5
nnet_dir=exp/xvector_nnets/$nnet_name
nnet=$nnet_dir/model_ep0070.pth

#tranfer nnets params
transfer_nnet_name=lresnet34_zir_e256_arc0.3_do0_adam_lr0.05_b512.v2
transfer_nnet_dir=exp/xvector_nnets/$transfer_nnet_name
transfer_nnet=$transfer_nnet_dir/model_ep0062.pth
transfer_feat_conf=conf/fbank80_16k.pyconf
transfer_feat=logfb

#back-end
lda_dim=200
plda_y_dim=150
plda_z_dim=200

plda_data=voxceleb2cat_combined
plda_type=splda
