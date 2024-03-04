library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
                 
    entity add32 is
        
        port (a : in std_logic_vector(31 DOWNTO 0);
              b : in std_logic_vector(31 DOWNTO 0);
              cin : in std_logic;
              sum1 : out std_logic_vector(31 DOWNTO 0);
              cout : out std_logic;
              overflow : out std_logic;
              underflow : out std_logic
        );
    end add32;
                 
    architecture arc of add32 is
        signal w_SIGNAL_BIT : std_logic;
        signal w_OVERFLOW : std_logic;
        signal w_UNDERFLOW : std_logic;
        signal c_0 : std_logic;
        signal c_1 : std_logic;
        signal c_2 : std_logic;
        signal c_3 : std_logic;
        signal c_4 : std_logic;
        signal c_5 : std_logic;
        signal c_6 : std_logic;
        signal c_7 : std_logic;
        signal c_8 : std_logic;
        signal c_9 : std_logic;
        signal c_10 : std_logic;
        signal c_11 : std_logic;
        signal c_12 : std_logic;
        signal c_13 : std_logic;
        signal c_14 : std_logic;
        signal c_15 : std_logic;
        signal c_16 : std_logic;
        signal c_17 : std_logic;
        signal c_18 : std_logic;
        signal c_19 : std_logic;
        signal c_20 : std_logic;
        signal c_21 : std_logic;
        signal c_22 : std_logic;
        signal c_23 : std_logic;
        signal c_24 : std_logic;
        signal c_25 : std_logic;
        signal c_26 : std_logic;
        signal c_27 : std_logic;
        signal c_28 : std_logic;
        signal c_29 : std_logic;
        signal c_30 : std_logic;
        signal w_SUM_OUT : std_logic_vector(31 DOWNTO 0);


        begin 
        D_adder0 : entity work.add1
        port map (
            a  => a(0),
            b  => b(0),
            cin  => cin,
            sum  => w_SUM_OUT(0),
            cout  => c_0
        );
 
        D_adder1 : entity work.add1
        port map (
            a  => a(1),
            b  => b(1),
            cin  => c_0,
            sum  => w_SUM_OUT(1),
            cout  => c_1
        );
 
        D_adder2 : entity work.add1
        port map (
            a  => a(2),
            b  => b(2),
            cin  => c_1,
            sum  => w_SUM_OUT(2),
            cout  => c_2
        );
 
        D_adder3 : entity work.add1
        port map (
            a  => a(3),
            b  => b(3),
            cin  => c_2,
            sum  => w_SUM_OUT(3),
            cout  => c_3
        );
 
        D_adder4 : entity work.add1
        port map (
            a  => a(4),
            b  => b(4),
            cin  => c_3,
            sum  => w_SUM_OUT(4),
            cout  => c_4
        );
 
        D_adder5 : entity work.add1
        port map (
            a  => a(5),
            b  => b(5),
            cin  => c_4,
            sum  => w_SUM_OUT(5),
            cout  => c_5
        );
 
        D_adder6 : entity work.add1
        port map (
            a  => a(6),
            b  => b(6),
            cin  => c_5,
            sum  => w_SUM_OUT(6),
            cout  => c_6
        );
 
        D_adder7 : entity work.add1
        port map (
            a  => a(7),
            b  => b(7),
            cin  => c_6,
            sum  => w_SUM_OUT(7),
            cout  => c_7
        );
 
        D_adder8 : entity work.add1
        port map (
            a  => a(8),
            b  => b(8),
            cin  => c_7,
            sum  => w_SUM_OUT(8),
            cout  => c_8
        );
 
        D_adder9 : entity work.add1
        port map (
            a  => a(9),
            b  => b(9),
            cin  => c_8,
            sum  => w_SUM_OUT(9),
            cout  => c_9
        );
 
        D_adder10 : entity work.add1
        port map (
            a  => a(10),
            b  => b(10),
            cin  => c_9,
            sum  => w_SUM_OUT(10),
            cout  => c_10
        );
 
        D_adder11 : entity work.add1
        port map (
            a  => a(11),
            b  => b(11),
            cin  => c_10,
            sum  => w_SUM_OUT(11),
            cout  => c_11
        );
 
        D_adder12 : entity work.add1
        port map (
            a  => a(12),
            b  => b(12),
            cin  => c_11,
            sum  => w_SUM_OUT(12),
            cout  => c_12
        );
 
        D_adder13 : entity work.add1
        port map (
            a  => a(13),
            b  => b(13),
            cin  => c_12,
            sum  => w_SUM_OUT(13),
            cout  => c_13
        );
 
        D_adder14 : entity work.add1
        port map (
            a  => a(14),
            b  => b(14),
            cin  => c_13,
            sum  => w_SUM_OUT(14),
            cout  => c_14
        );
 
        D_adder15 : entity work.add1
        port map (
            a  => a(15),
            b  => b(15),
            cin  => c_14,
            sum  => w_SUM_OUT(15),
            cout  => c_15
        );
 
        D_adder16 : entity work.add1
        port map (
            a  => a(16),
            b  => b(16),
            cin  => c_15,
            sum  => w_SUM_OUT(16),
            cout  => c_16
        );
 
        D_adder17 : entity work.add1
        port map (
            a  => a(17),
            b  => b(17),
            cin  => c_16,
            sum  => w_SUM_OUT(17),
            cout  => c_17
        );
 
        D_adder18 : entity work.add1
        port map (
            a  => a(18),
            b  => b(18),
            cin  => c_17,
            sum  => w_SUM_OUT(18),
            cout  => c_18
        );
 
        D_adder19 : entity work.add1
        port map (
            a  => a(19),
            b  => b(19),
            cin  => c_18,
            sum  => w_SUM_OUT(19),
            cout  => c_19
        );
 
        D_adder20 : entity work.add1
        port map (
            a  => a(20),
            b  => b(20),
            cin  => c_19,
            sum  => w_SUM_OUT(20),
            cout  => c_20
        );
 
        D_adder21 : entity work.add1
        port map (
            a  => a(21),
            b  => b(21),
            cin  => c_20,
            sum  => w_SUM_OUT(21),
            cout  => c_21
        );
 
        D_adder22 : entity work.add1
        port map (
            a  => a(22),
            b  => b(22),
            cin  => c_21,
            sum  => w_SUM_OUT(22),
            cout  => c_22
        );
 
        D_adder23 : entity work.add1
        port map (
            a  => a(23),
            b  => b(23),
            cin  => c_22,
            sum  => w_SUM_OUT(23),
            cout  => c_23
        );
 
        D_adder24 : entity work.add1
        port map (
            a  => a(24),
            b  => b(24),
            cin  => c_23,
            sum  => w_SUM_OUT(24),
            cout  => c_24
        );
 
        D_adder25 : entity work.add1
        port map (
            a  => a(25),
            b  => b(25),
            cin  => c_24,
            sum  => w_SUM_OUT(25),
            cout  => c_25
        );
 
        D_adder26 : entity work.add1
        port map (
            a  => a(26),
            b  => b(26),
            cin  => c_25,
            sum  => w_SUM_OUT(26),
            cout  => c_26
        );
 
        D_adder27 : entity work.add1
        port map (
            a  => a(27),
            b  => b(27),
            cin  => c_26,
            sum  => w_SUM_OUT(27),
            cout  => c_27
        );
 
        D_adder28 : entity work.add1
        port map (
            a  => a(28),
            b  => b(28),
            cin  => c_27,
            sum  => w_SUM_OUT(28),
            cout  => c_28
        );
 
        D_adder29 : entity work.add1
        port map (
            a  => a(29),
            b  => b(29),
            cin  => c_28,
            sum  => w_SUM_OUT(29),
            cout  => c_29
        );
 
        D_adder30 : entity work.add1
        port map (
            a  => a(30),
            b  => b(30),
            cin  => c_29,
            sum  => w_SUM_OUT(30),
            cout  => c_30
        );
 
        D_adder31 : entity work.add1
        port map (
            a  => a(31),
            b  => b(31),
            cin  => c_30,
            sum  => w_SIGNAL_BIT,
            cout  => cout
        );

        w_SUM_OUT(31) <= w_SIGNAL_BIT;           
        w_UNDERFLOW <= a(31) and b(31) and not w_SIGNAL_BIT;
        sum1 <= "10000000000000000000000000000000" when (w_UNDERFLOW = '1') else 
                "01111111111111111111111111111111" when (w_OVERFLOW= '1') else 
                w_SUM_OUT;
        overflow <=  w_OVERFLOW; 
        underflow <= w_UNDERFLOW;
        
    end arc;