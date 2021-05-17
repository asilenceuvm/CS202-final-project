
  .globl main
main:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $16384, %rdi
  movq $16, %rsi
  callq initialize
  movq rootstack_begin(%rip), %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15

  jmp main_start
label_832:
  movq free_ptr(%rip), %rdx
  addq $112, free_ptr(%rip)
  movq %rdx, %r11
  movq $1048219, 0(%r11)
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -136(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -144(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -96(%r15), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -80(%r15), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%r15), %rax
  movq %rax, 72(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 80(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -64(%r15), %rax
  movq %rax, 88(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 96(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -104(%r15), %rax
  movq %rax, 104(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, %r11
  movq 96(%r11), %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_833:
  movq $0, %rdx
  jmp label_832
label_834:
  movq %r15, %rdi
  movq $112, %rsi
  callq collect
  jmp label_832
label_835:
  movq free_ptr(%rip), %rdx
  addq $104, free_ptr(%rip)
  movq %rdx, %r11
  movq $523929, 0(%r11)
  movq %rdx, %r11
  movq -112(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -152(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -128(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -72(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -88(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -56(%r15), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -120(%r15), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -160(%r15), %rax
  movq %rax, 72(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -176(%r15), %rax
  movq %rax, 80(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 88(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -168(%r15), %rax
  movq %rax, 96(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, -48(%r15)
  movq -136(%r15), %rax
  movq %rax, -136(%r15)
  movq -32(%r15), %rax
  movq %rax, -32(%r15)
  movq -24(%r15), %rax
  movq %rax, -24(%r15)
  movq -16(%r15), %rax
  movq %rax, -16(%r15)
  movq -144(%r15), %rax
  movq %rax, -144(%r15)
  movq -96(%r15), %rax
  movq %rax, -96(%r15)
  movq -80(%r15), %rax
  movq %rax, -80(%r15)
  movq -40(%r15), %rax
  movq %rax, -40(%r15)
  movq -8(%r15), %rax
  movq %rax, -8(%r15)
  movq -64(%r15), %rax
  movq %rax, -64(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -104(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $112, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_833
  jmp label_834
label_836:
  movq $0, %rdx
  jmp label_835
label_837:
  movq %r15, %rdi
  movq $104, %rsi
  callq collect
  jmp label_835
label_838:
  movq free_ptr(%rip), %rdx
  addq $96, free_ptr(%rip)
  movq %rdx, %r11
  movq $261783, 0(%r11)
  movq %rdx, %r11
  movq -128(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -56(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -160(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -112(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -72(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -136(%r15), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -88(%r15), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -152(%r15), %rax
  movq %rax, 72(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 80(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -120(%r15), %rax
  movq %rax, 88(%r11)
  movq $0, %rcx
  movq %rdx, -136(%r15)
  movq -136(%r15), %rax
  movq %rax, -112(%r15)
  movq -32(%r15), %rax
  movq %rax, -152(%r15)
  movq -24(%r15), %rax
  movq %rax, -48(%r15)
  movq -16(%r15), %rax
  movq %rax, -128(%r15)
  movq -144(%r15), %rax
  movq %rax, -72(%r15)
  movq -96(%r15), %rax
  movq %rax, -88(%r15)
  movq -80(%r15), %rax
  movq %rax, -56(%r15)
  movq -40(%r15), %rax
  movq %rax, -120(%r15)
  movq -8(%r15), %rax
  movq %rax, -160(%r15)
  movq -64(%r15), %rax
  movq %rax, -176(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -168(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $104, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_836
  jmp label_837
label_839:
  movq $0, %rdx
  jmp label_838
label_840:
  movq %r15, %rdi
  movq $96, %rsi
  callq collect
  jmp label_838
label_841:
  movq free_ptr(%rip), %rdx
  addq $88, free_ptr(%rip)
  movq %rdx, %r11
  movq $130709, 0(%r11)
  movq %rdx, %r11
  movq -112(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -56(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -72(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -120(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -128(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -136(%r15), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 72(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -88(%r15), %rax
  movq %rax, 80(%r11)
  movq $0, %rcx
  movq %rdx, -32(%r15)
  movq -32(%r15), %rax
  movq %rax, -128(%r15)
  movq -24(%r15), %rax
  movq %rax, -56(%r15)
  movq -16(%r15), %rax
  movq %rax, -160(%r15)
  movq -144(%r15), %rax
  movq %rax, -112(%r15)
  movq -96(%r15), %rax
  movq %rax, -48(%r15)
  movq -80(%r15), %rax
  movq %rax, -72(%r15)
  movq -40(%r15), %rax
  movq %rax, -136(%r15)
  movq -8(%r15), %rax
  movq %rax, -88(%r15)
  movq -64(%r15), %rax
  movq %rax, -152(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -120(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $96, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_839
  jmp label_840
label_842:
  movq $0, %rdx
  jmp label_841
label_843:
  movq %r15, %rdi
  movq $88, %rsi
  callq collect
  jmp label_841
label_844:
  movq free_ptr(%rip), %rdx
  addq $80, free_ptr(%rip)
  movq %rdx, %r11
  movq $65171, 0(%r11)
  movq %rdx, %r11
  movq -136(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -56(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -88(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -72(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 64(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -112(%r15), %rax
  movq %rax, 72(%r11)
  movq $0, %rcx
  movq %rdx, -24(%r15)
  movq -24(%r15), %rax
  movq %rax, -112(%r15)
  movq -16(%r15), %rax
  movq %rax, -48(%r15)
  movq -144(%r15), %rax
  movq %rax, -56(%r15)
  movq -96(%r15), %rax
  movq %rax, -72(%r15)
  movq -80(%r15), %rax
  movq %rax, -120(%r15)
  movq -40(%r15), %rax
  movq %rax, -128(%r15)
  movq -8(%r15), %rax
  movq %rax, -32(%r15)
  movq -64(%r15), %rax
  movq %rax, -136(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -88(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $88, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_842
  jmp label_843
label_845:
  movq $0, %rdx
  jmp label_844
label_846:
  movq %r15, %rdi
  movq $80, %rsi
  callq collect
  jmp label_844
label_847:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $32401, 0(%r11)
  movq %rdx, %r11
  movq -136(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -72(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -56(%r15), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, -16(%r15)
  movq -16(%r15), %rax
  movq %rax, -136(%r15)
  movq -144(%r15), %rax
  movq %rax, -56(%r15)
  movq -96(%r15), %rax
  movq %rax, -24(%r15)
  movq -80(%r15), %rax
  movq %rax, -88(%r15)
  movq -40(%r15), %rax
  movq %rax, -72(%r15)
  movq -8(%r15), %rax
  movq %rax, -48(%r15)
  movq -64(%r15), %rax
  movq %rax, -32(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -112(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $80, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_845
  jmp label_846
label_848:
  movq $0, %rdx
  jmp label_847
label_849:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_847
label_850:
  movq free_ptr(%rip), %rdx
  addq $64, free_ptr(%rip)
  movq %rdx, %r11
  movq $16015, 0(%r11)
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -144(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -136(%r15), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, -144(%r15)
  movq -144(%r15), %rax
  movq %rax, -136(%r15)
  movq -96(%r15), %rax
  movq %rax, -24(%r15)
  movq -80(%r15), %rax
  movq %rax, -48(%r15)
  movq -40(%r15), %rax
  movq %rax, -16(%r15)
  movq -8(%r15), %rax
  movq %rax, -32(%r15)
  movq -64(%r15), %rax
  movq %rax, -72(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -56(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $72, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_848
  jmp label_849
label_851:
  movq $0, %rdx
  jmp label_850
label_852:
  movq %r15, %rdi
  movq $64, %rsi
  callq collect
  jmp label_850
label_853:
  movq free_ptr(%rip), %rdx
  addq $56, free_ptr(%rip)
  movq %rdx, %r11
  movq $7821, 0(%r11)
  movq %rdx, %r11
  movq -136(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -96(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, -96(%r15)
  movq -96(%r15), %rax
  movq %rax, -48(%r15)
  movq -80(%r15), %rax
  movq %rax, -32(%r15)
  movq -40(%r15), %rax
  movq %rax, -144(%r15)
  movq -8(%r15), %rax
  movq %rax, -24(%r15)
  movq -64(%r15), %rax
  movq %rax, -16(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -136(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $64, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_851
  jmp label_852
label_854:
  movq $0, %rdx
  jmp label_853
label_855:
  movq %r15, %rdi
  movq $56, %rsi
  callq collect
  jmp label_853
label_856:
  movq free_ptr(%rip), %rdx
  addq $48, free_ptr(%rip)
  movq %rdx, %r11
  movq $3723, 0(%r11)
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -96(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, -80(%r15)
  movq -80(%r15), %rax
  movq %rax, -136(%r15)
  movq -40(%r15), %rax
  movq %rax, -96(%r15)
  movq -8(%r15), %rax
  movq %rax, -16(%r15)
  movq -64(%r15), %rax
  movq %rax, -32(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -24(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $56, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_854
  jmp label_855
label_857:
  movq $0, %rdx
  jmp label_856
label_858:
  movq %r15, %rdi
  movq $48, %rsi
  callq collect
  jmp label_856
label_859:
  movq free_ptr(%rip), %rdx
  addq $40, free_ptr(%rip)
  movq %rdx, %r11
  movq $1673, 0(%r11)
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, -40(%r15)
  movq -40(%r15), %rax
  movq %rax, -16(%r15)
  movq -8(%r15), %rax
  movq %rax, -24(%r15)
  movq -64(%r15), %rax
  movq %rax, -96(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -32(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $48, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_857
  jmp label_858
label_860:
  movq $0, %rdx
  jmp label_859
label_861:
  movq %r15, %rdi
  movq $40, %rsi
  callq collect
  jmp label_859
label_862:
  movq free_ptr(%rip), %rdx
  addq $32, free_ptr(%rip)
  movq %rdx, %r11
  movq $647, 0(%r11)
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, -8(%r15)
  movq -8(%r15), %rax
  movq %rax, -16(%r15)
  movq -64(%r15), %rax
  movq %rax, -40(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -24(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $40, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_860
  jmp label_861
label_863:
  movq $0, %rdx
  jmp label_862
label_864:
  movq %r15, %rdi
  movq $32, %rsi
  callq collect
  jmp label_862
label_865:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $133, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, -64(%r15)
  movq -64(%r15), %rax
  movq %rax, -8(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -16(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $32, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_863
  jmp label_864
label_866:
  movq $0, %rdx
  jmp label_865
label_867:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_865
label_868:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, -104(%r15)
  movq $42, %rbx
  movq -104(%r15), %rax
  movq %rax, -8(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $24, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_866
  jmp label_867
label_869:
  movq $0, %rdx
  jmp label_868
label_870:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_868
main_start:
  movq $1, %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $16, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_869
  jmp label_870
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $0, %rsp
  subq $176, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
