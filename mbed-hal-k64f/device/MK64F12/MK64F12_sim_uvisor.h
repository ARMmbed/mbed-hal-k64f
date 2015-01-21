#ifndef __HW_SIM_REGISTERS_UVISOR_H__
#define __HW_SIM_REGISTERS_UVISOR_H__

/* Apparently, the Freescale MK64F12 SIM registers show a behavior
 * which is different from the documented one (see K64P144M120SF5RM,
 * Rev. 2, January 2014). SIM_SCGx registers can be written only in
 * supervisor mode, differently from what documented.
 *
 * Here all the macros for bitband access to these peripherals are
 * defined. The macros use an SVCall to handle the write to the
 * desired bitbanded address. The uvisor checks their legitimacy
 * before actually writing to that address.
 *
 * The uvisor is present by default, but if it is not enabled, the
 * write to the register is performed as usual */

#if defined(K64F12_SERIES) && (defined(__GNUC__) && !defined(__ARMCC_VERSION))

#include "MK64F12.h"
#include "fsl_bitaccess.h"

/* bitband address from normale address and bit position */
#define BITBAND_ADDRESS32(Reg,Bit) ((uint32_t volatile*)(0x42000000u +\
            (32u*((uint32_t)(Reg) - (uint32_t)0x40000000u))          +\
            (4u*((uint32_t)(Bit)))))
#define BITBAND_ADDRESS16(Reg,Bit) ((uint16_t volatile*)(0x42000000u +\
            (32u*((uint32_t)(Reg) - (uint32_t)0x40000000u))          +\
            (4u*((uint32_t)(Bit)))))
#define BITBAND_ADDRESS8(Reg,Bit)  ((uint8_t  volatile*)(0x42000000u +\
            (32u*((uint32_t)(Reg) - (uint32_t)0x40000000u))          +\
            (4u*((uint32_t)(Bit)))))

/* uvisor mode */
extern const uint32_t __uvisor_mode;

/* translate a bitband access in an SVCall if the uvisor is enabled
 * normal bitband access is provided otherwise */
static inline void uvisor_bitband(uint32_t *addr, uint32_t val)
{
    if (__uvisor_mode == 0) {
        *addr = val;
    }
    else {
        register uint32_t __r0 __asm__("r0") = (uint32_t) addr;
        register uint32_t __r1 __asm__("r1") = (uint32_t) val;
        __asm__ volatile(
            "svc  #0\n"
            :: "r" (__r0), "r" (__r1)
	);
    }
}

/* SIM_SCGC1 */

#undef  BW_SIM_SCGC1_UART4
#define BW_SIM_SCGC1_UART4(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC1_ADDR(x), BP_SIM_SCGC1_UART4), v)

#undef  BW_SIM_SCGC1_UART5
#define BW_SIM_SCGC1_UART5(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC1_ADDR(x), BP_SIM_SCGC1_UART5), v)

/* SIM_SCGC4 */

#undef  BW_SIM_SCGC4_UART0
#define BW_SIM_SCGC4_UART0(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC4_ADDR(x), BP_SIM_SCGC4_UART0), v)

#undef  BW_SIM_SCGC4_UART1
#define BW_SIM_SCGC4_UART1(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC4_ADDR(x), BP_SIM_SCGC4_UART1), v)

#undef  BW_SIM_SCGC4_UART2
#define BW_SIM_SCGC4_UART2(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC4_ADDR(x), BP_SIM_SCGC4_UART2), v)

#undef  BW_SIM_SCGC4_UART3
#define BW_SIM_SCGC4_UART3(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC4_ADDR(x), BP_SIM_SCGC4_UART3), v)

/* SIM_SCGC5 */

#undef  BW_SIM_SCGC5_PORTA
#define BW_SIM_SCGC5_PORTA(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC5_ADDR(x), BP_SIM_SCGC5_PORTA), v)

#undef  BW_SIM_SCGC5_PORTB
#define BW_SIM_SCGC5_PORTB(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC5_ADDR(x), BP_SIM_SCGC5_PORTB), v)

#undef  BW_SIM_SCGC5_PORTC
#define BW_SIM_SCGC5_PORTC(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC5_ADDR(x), BP_SIM_SCGC5_PORTC), v)

#undef  BW_SIM_SCGC5_PORTD
#define BW_SIM_SCGC5_PORTD(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC5_ADDR(x), BP_SIM_SCGC5_PORTD), v)

#undef  BW_SIM_SCGC5_PORTE
#define BW_SIM_SCGC5_PORTE(x, v) \
  uvisor_bitband(BITBAND_ADDRESS32(HW_SIM_SCGC5_ADDR(x), BP_SIM_SCGC5_PORTE), v)

#endif/*defined(K64F12_SERIES) && defined(__GNUC__)*/

#endif/*__HW_SIM_REGISTERS_UVISOR_H__*/
