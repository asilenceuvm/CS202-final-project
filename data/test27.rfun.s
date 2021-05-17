
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

  jmp main_start
label_556:
  movq free_ptr(%rip), %rdx
  addq $136, free_ptr(%rip)
  movq %rdx, %r11
  movq $8388513, 0(%r11)
  movq %rdx, %r11
  movq -96(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -128(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -80(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -56(%r15), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -64(%r15), %rax
  movq %rax, 72(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -112(%r15), %rax
  movq %rax, 80(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -88(%r15), %rax
  movq %rax, 88(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -104(%r15), %rax
  movq %rax, 96(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -120(%r15), %rax
  movq %rax, 104(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%r15), %rax
  movq %rax, 112(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 120(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -72(%r15), %rax
  movq %rax, 128(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, %r11
  movq 40(%r11), %rdx
  movq %rdx, %r11
  movq 32(%r11), %rdx
  movq %rdx, %r11
  movq 24(%r11), %rdx
  movq %rdx, %r11
  movq 16(%r11), %rdx
  movq %rdx, %r11
  movq 8(%r11), %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_557:
  movq $0, %rdx
  jmp label_556
label_558:
  movq %r15, %rdi
  movq $136, %rsi
  callq collect
  jmp label_556
label_559:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $32657, 0(%r11)
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -64(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%r15), %rax
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
  movq -24(%r15), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -56(%r15), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%r15), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, -96(%r15)
  movq %rdx, -128(%r15)
  movq %rdx, -24(%r15)
  movq %rdx, -8(%r15)
  movq %rdx, -16(%r15)
  movq %rdx, -80(%r15)
  movq %rdx, -56(%r15)
  movq %rdx, -48(%r15)
  movq %rdx, -64(%r15)
  movq %rdx, -112(%r15)
  movq %rdx, -88(%r15)
  movq %rdx, -104(%r15)
  movq %rdx, -120(%r15)
  movq %rdx, -40(%r15)
  movq %rdx, -32(%r15)
  movq %rdx, -72(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $136, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_557
  jmp label_558
label_560:
  movq $0, %rdx
  jmp label_559
label_561:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_559
label_562:
  movq free_ptr(%rip), %rdx
  addq $40, free_ptr(%rip)
  movq %rdx, %r11
  movq $1929, 0(%r11)
  movq %rdx, %r11
  movq -32(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%r15), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, -8(%r15)
  movq %rdx, -64(%r15)
  movq %rdx, -40(%r15)
  movq %rdx, -16(%r15)
  movq %rdx, -32(%r15)
  movq %rdx, -24(%r15)
  movq %rdx, -56(%r15)
  movq %rdx, -48(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $72, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_560
  jmp label_561
label_563:
  movq $0, %rdx
  jmp label_562
label_564:
  movq %r15, %rdi
  movq $40, %rsi
  callq collect
  jmp label_562
label_565:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $389, 0(%r11)
  movq %rdx, %r11
  movq -16(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, -32(%r15)
  movq %rdx, -8(%r15)
  movq %rdx, -16(%r15)
  movq %rdx, -24(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $40, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_563
  jmp label_564
label_566:
  movq $0, %rdx
  jmp label_565
label_567:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_565
label_568:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, -16(%r15)
  movq %rdx, -8(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $24, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_566
  jmp label_567
label_569:
  movq $0, %rdx
  jmp label_568
label_570:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_568
main_start:
  movq $42, %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $16, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_569
  jmp label_570
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $0, %rsp
  subq $128, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
